"""Scan selection and full-resolution spectrum export for local and VM routes."""
import io
from pathlib import Path
import numpy as np
from django.http import JsonResponse,FileResponse
from django.views.decorators.http import require_POST
from plugins.read_data import ReadData
from plugins.column_preview import build_column_preview
from plugins.column_correction import selection_from_request,sign_qc_result
from plugins.frank_preview import original_file_qc
from django.template.loader import render_to_string


@require_POST
def apply_columns_view(request):
    filename=Path(request.POST.get('dataset_name','')).name
    if not filename:return JsonResponse({'error':'Upload a measurement first.'},status=400)
    selection=selection_from_request(request.POST)
    from plugins.column_correction import pending_upload_path
    try:
        path = pending_upload_path(request, filename)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)
    result=original_file_qc(path,source=request.POST.get('Source','SYNCHROTRON'),
        column_selection=selection,element=request.POST.get('Element'),edge=request.POST.get('Edge'))
    if not result['available']:return JsonResponse({'error':result['error']},status=400)
    token=sign_qc_result(path,result,selection)
    return JsonResponse(dict(html=render_to_string('landing/frank_panel.html',{'frank_qc':result}),
        confirmation=token,selection=result['selection'],source=result['source'],element=result['element'],edge=result['edge'],
        energy_min=result['energy_min'],energy_max=result['energy_max'],report=result['report']))


@require_POST
def scan_columns_view(request):
    filename=Path(request.POST.get('dataset_name','')).name
    if not filename: return JsonResponse({'error':'Upload a measurement first.'},status=400)
    try:
        reader=ReadData(preview_columns=True,scan_number=request.POST.get('scan','0'),
                        source=request.POST.get('Source','SYNCHROTRON'))
        from plugins.column_correction import pending_upload_path
        reader.process_data(pending_upload_path(request, filename))
        return JsonResponse(build_column_preview(reader))
    except (ValueError,OSError,AttributeError,KeyError,IndexError) as exc:
        return JsonResponse({'error':str(exc)},status=400)


@require_POST
def selected_spectrum_export(request):
    filename=Path(request.POST.get('dataset_name','')).name
    if not filename: return JsonResponse({'error':'Upload a measurement first.'},status=400)
    reader=ReadData(column_selection=selection_from_request(request.POST),
                    update_erange=request.POST if request.POST.get('apply_range')=='yes' else None,
                    source=request.POST.get('Source','SYNCHROTRON'))
    try:
        reader.process_data(Path('temp')/filename)
        output=io.StringIO()
        selection=reader.meta_data_dict['Column_selection']
        for key,value in selection.items(): output.write('# '+key+': '+str(value)+'\n')
        output.write('energy_eV,mu\n')
        np.savetxt(output,reader.data[[0,2]].T,delimiter=',',fmt='%.15g')
        return FileResponse(io.BytesIO(output.getvalue().encode('utf-8')),as_attachment=True,
                            filename=Path(filename).stem+'_selected_spectrum.csv',content_type='text/csv')
    except (ValueError,OSError,AttributeError,KeyError,IndexError) as exc:
        return JsonResponse({'error':str(exc)},status=400)
    finally:
        import matplotlib.pyplot as plt
        if hasattr(reader,'fig_raw_data'): plt.close(reader.fig_raw_data)

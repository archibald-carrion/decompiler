from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def assembly_to_c(request):
    c_output = None
    assembly_code = ''
    if request.method == 'POST':
        assembly_code = request.POST.get('assembly_code', '')
        # For now, return a fixed C output
        c_output = """int main() {\n    // Example C code\n    return 0;\n}"""
    return render(request, 'assembly_form.html', {
        'assembly_code': assembly_code,
        'c_output': c_output
    })

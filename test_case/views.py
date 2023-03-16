# import django packages
from django.shortcuts import render, redirect
from django.contrib import messages

# import model and form
from .models import CSV
from .form import PhoneNumber

# for fun on interface
from test_case.settings import GROSEV_IS_ANGRY, GROSEV_IS_WAITING, KUDRYAVZEV


# to avoid resubmit form on reload page
def start_page(request):
    images = {
       'warning': GROSEV_IS_ANGRY,
       'info': KUDRYAVZEV
    }
    try:
        url = images[request.session['status']]
        del request.session['status']
    except Exception as ex:
        url = GROSEV_IS_WAITING
    form = PhoneNumber()
    return render(request, 'page.html', {
        'form': form,
        'url': url
    })


def search(request):
    if request.method == 'POST':
        phone_number_ = request.POST['phone_number']
        if len(phone_number_) == 10:
            city_code = phone_number_[:3]
            phone_number = int(phone_number_[3:])
            if CSV.objects.filter(city_code=city_code).exists():
                csv_rows = CSV.objects.filter(city_code=city_code).all()
                for row in csv_rows:
                    if row.start == phone_number or\
                        row.finish == phone_number or\
                            row.start < phone_number < row.finish:
                        messages.info(request, f'Номер: {phone_number_}')
                        messages.info(request, f'Регион: {row.geo}')
                        messages.info(request, f'Оператор: {row.operator}')
                        request.session['status'] = 'info'
                        return redirect('start_page')
                messages.warning(request, 'Нам неизвестен такой номер!')
                request.session['status'] = 'warning'
                return redirect('start_page')
            else:
                messages.warning(request, 'Нет такого кода города. ')
        else:
            messages.warning(
                request, 'Номер телефона должен состоять из 10 цифр. ')
        request.session['status'] = 'warning'
        return redirect('start_page')
    return redirect('start_page')

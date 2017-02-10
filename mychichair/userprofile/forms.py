# encoding: utf-8
from __future__ import unicode_literals

from django import forms

from .i18n import AddressMetaForm, get_address_form_class


def get_address_form(data, country_code, initial=None, instance=None, **kwargs):
    country_form = AddressMetaForm(data, initial=initial)
    preview = False

    if country_form.is_valid():
        country_code = country_form.cleaned_data['country']
        preview = country_form.cleaned_data['preview']

    address_form_class = get_address_form_class(country_code)

    if "SN" == country_code.upper():
        initial = {'street_address_1': 'RAS', 'street_address_2': 'RAS', 'city': 'Dakar', 'postal_code': '10700'}
    print(initial)

    if not preview and instance is not None:
        address_form_class = get_address_form_class(
            instance.country.code)
        print('no preview', initial)
        address_form = address_form_class(data, instance=instance, initial=initial, **kwargs)
    else:
        initial_address = (
            initial if not preview
            else data.dict() if data is not None else data)
        print('preview', initial_address, initial)
        address_form = address_form_class(not preview and data or None, initial=initial_address, **kwargs)

    if "SN" == country_code.upper():
        format_fields_for_sn(address_form)

    return address_form, preview


def format_fields_for_sn(address_form):
    for field in ['sorting_code', 'city', 'sorting_code', 'postal_code', 'company_name', 'country_area', 'city_area',
                  'street_address_1', 'street_address_2']:
        if field in address_form.fields:
            address_form.fields[field].widget = forms.HiddenInput()

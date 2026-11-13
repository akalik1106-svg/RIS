from os import path

from flask import Blueprint, render_template, request, url_for

from auth.access import group_required
from database.sql_provider import SQLProvider
from query_bp.module_route import balance_query, call_query, sub_query

blueprint_query = Blueprint('query', __name__, template_folder='templates')
provider = SQLProvider(path.join(path.dirname(__file__), 'sql'))


def _render(res_info, title):
    back_url = url_for('query.request_handler')
    if res_info.status:
        return render_template('result_table.html', title=title, columns=res_info.columns,
                               rows=res_info.result, back_url=back_url)
    return render_template('err_query.html', error_message=res_info.error_message, back_url=back_url)


def _form(title, fields):
    return render_template('query_form.html', title=title, fields=fields)


@blueprint_query.route('/', methods=['GET'])
@group_required
def request_handler():
    return render_template('queries.html')


@blueprint_query.route('/call', methods=['GET', 'POST'])
@group_required
def call_handler():
    if request.method == 'GET':
        return _form('Поиск начала звонка и объёма по ID', [
            {'name': 'callind_id', 'label': 'ID звонка',
             'placeholder': 'Введите callind_id', 'inputmode': 'numeric'}
        ])
    return _render(call_query(request.form, provider), 'Начало звонка и объём')


@blueprint_query.route('/sub', methods=['GET', 'POST'])
@group_required
def sub_handler():
    if request.method == 'GET':
        return _form('Данные абонента по номеру телефона', [
            {'name': 'phone_number', 'label': 'Номер телефона',
             'placeholder': 'Введите номер телефона', 'inputmode': 'tel'}
        ])
    return _render(sub_query(request.form, provider), 'Данные абонента')


@blueprint_query.route('/balance', methods=['GET', 'POST'])
@group_required
def balance_handler():
    if request.method == 'GET':
        return _form('История изменения баланса', [
            {'name': 'sub_id', 'label': 'ID абонента',
             'placeholder': 'Введите sub_id', 'inputmode': 'numeric'},
            {'name': 'update_date', 'label': 'Дата обновления',
             'placeholder': 'ГГГГ-ММ-ДД', 'inputmode': 'numeric'}
        ])
    return _render(balance_query(request.form, provider), 'Баланс до и после обновления')
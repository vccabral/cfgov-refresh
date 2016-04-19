import os

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.http import JsonResponse
from govdelivery.api import GovDelivery

from core.utils import extract_answers_from_request

ACCOUNT_CODE = os.environ.get('GOVDELIVERY_ACCOUNT_CODE')
REQUIRED_PARAMS_GOVDELIVERY = ['email', 'code']


@csrf_exempt
@require_http_methods(['POST'])
def govdelivery_subscribe(request):
    """
    View that checks to see if the request is AJAX, attempts to subscribe
    the user, then either redirects to an error/success page (non-AJAX) or
    in the case of AJAX, returns some JSON to tell the front-end.
    """
    is_ajax = request.is_ajax()
    if is_ajax:
        passing_response = JsonResponse({'result': 'pass'})
        failing_response = JsonResponse({'result': 'fail'})
    else:
        passing_response = redirect('govdelivery:success')
        failing_response = redirect('govdelivery:server_error')
    for required_param in REQUIRED_PARAMS_GOVDELIVERY:
        if required_param not in request.POST or not request.POST[required_param]:
            return failing_response if is_ajax else \
                redirect('govdelivery:user_error')
    email_address = request.POST['email']
    codes = request.POST.getlist('code')
    gd = GovDelivery(account_code=ACCOUNT_CODE)
    try:
        subscription_response = gd.set_subscriber_topics(email_address, codes)
        if subscription_response.status_code != 200:
            return failing_response
    except Exception:
        return failing_response
    answers = extract_answers_from_request(request)
    for question_id, answer_text in answers:
        response = gd.set_subscriber_answers_to_question(email_address,
                                                         question_id,
                                                         answer_text)
    return passing_response


REGSGOV_API_KEY = os.environ.get('REGSGOV_API_KEY')
REQUIRED_PARAMS_REGSGOV = ['document_id', 'comment', 'first_name', 'last_name']


@csrf_exempt
@require_http_methods(['POST'])
def regsgov_comment(request):
    """
    View that checks to see if the request is AJAX, attempts to submit
    the comment, then either redirects to an error/success page (non-AJAX) or
    in the case of AJAX, returns some JSON to tell the front-end.
    """
    is_ajax = request.is_ajax()
    if is_ajax:
        passing_response = JsonResponse({'result': 'pass'})
        failing_response = JsonResponse({'result': 'fail'})
    else:
        passing_response = redirect('reg_comment:success')
        failing_response = redirect('reg_comment:server_error')
    for required_param in REQUIRED_PARAMS_REGSGOV:
        if required_param not in request.POST or not request.POST[required_param]:
            return failing_response if is_ajax else \
                redirect('reg_comment:user_error')
    document_id = request.POST['document_id']
    try:
        submission_response = submit_comment(api_key=REGSGOV_API_KEY,
                                             document_id, request.POST)
        if submission_response.status_code != 200:
            return failing_response
    except Exception:
        return failing_response
    """
    answers = extract_answers_from_request(request)
    for question_id, answer_text in answers:
        response = gd.set_subscriber_answers_to_question(email_address,
                                                         question_id,
                                                         answer_text)
    """

    return passing_response


def submit_comment(api_key, document_id, payload):
    

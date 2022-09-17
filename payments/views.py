from django.shortcuts import render, redirect
from django.conf import settings # new
from django.http.response import JsonResponse # new
from django.views.decorators.csrf import csrf_exempt # new
from exams.models import Student, PAYMENT_STATUS_OPTIONS, SUCCESS, CANCELLED, NONE

import stripe 

def payment_index(request):
    print('DEBUG: in payment_index2')
    return render(request, 'payments/index.html', {})

def success(request):
    # in the success view, we need to modify the user model
    # set flag so that the user is a paid user, giving them the access to all the features
    # in the exam views, we need to make sure the user is a paid user, can't just set the frontend (since users can navigate to URLs)

    user = request.user
    student:Student = Student.objects.get(user=user)
    if not student:
        print('ERROR: in payment success: not able to find student')
    else:
        student.is_premium = True 
        student.payment_status = SUCCESS
        student.save()

    # redirects to the exam-list-view (needs to pass parameter of the payment success)
    return redirect('exams:exam-list-view')

def cancelled(request):
    user = request.user
    student:Student = Student.objects.get(user=user)
    if not student:
        print('ERROR: in payment success: not able to find student')
    else:
        student.payment_status = CANCELLED
        student.save()

    # redirects to the exam-list-view (needs to pass parameter of the payment success)
    return redirect('exams:exam-list-view')

# new
@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = settings.DOMAIN_URL
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                # success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                success_url=domain_url + '/payments/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + '/payments/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': 'price_1LdTOwH5qgqT3cKZ34qKZHuQ',
                        'quantity': 1,
                    }
                ]
                # line_items=[
                #     {
                #         'name': 'Test Product',
                #         'quantity': 1,
                #         'currency': 'usd',
                #         'amount': '2000',
                #     }
                # ]
            )

            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            print('error: ', e)
            return JsonResponse({'error': str(e)})
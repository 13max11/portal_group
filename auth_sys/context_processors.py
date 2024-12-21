from django.contrib.auth import get_user_model
from .models import SavedAccount

def saved_accounts(request):
    context = {}
    if request.user.is_authenticated:
        saved_accounts = []
        for saved_account in SavedAccount.objects.filter(user=request.user):
            try:
                account = get_user_model().objects.get(username=saved_account.username)
                saved_accounts.append(account)
            except:
                continue
        context['saved_accounts'] = saved_accounts
    return context 
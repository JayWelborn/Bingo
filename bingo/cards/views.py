from django.shortcuts import redirect
from django.views import generic as g
from django.urls import reverse

from .models import BingoCard


# Create your views here.
class CardListView(g.ListView):
    """View that displays a list of cards.

    Attributes:
        model: Model to list
        context_object_name: Name used in template for readability
        queryset: Sort list of cards by most recent first
        paginate_by: Break list into pages for convenient viewing
        template_name: Template used to render list

    Methods:
        get_queryset: Filter out private cards if user is not authenticated

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-display/#listview

    """

    model = BingoCard
    context_object_name = 'bingocards'
    queryset = BingoCard.objects.order_by('-created_date')
    paginate_by = 8
    template_name = 'cards/card_list.html'

    def get_queryset(self):
        """
        Filter private cards out if user is not authenticated
        """
        queryset = super(CardListView, self).get_queryset()

        if self.request.user.is_authenticated:
            return queryset

        else:
            return queryset.filter(private=False)


class CardDetailView(g.DetailView):
    """Display full Bingo Card to play.

    Attributes:
        model: The model that will be rendered by the view.
        context_object_name: Name of object to be passed to template
        template_name: HTML template that will render data.

    Methods:
        get: redirect to login-required view if unauthenticated user attempts
            to access private card.

    References:
        * https://docs.djangoproject.com/en/1.11/ref/class-based-views/generic-display/#detailview

    """

    model = BingoCard
    context_object_name = 'card'
    template_name = 'cards/card_detail.html'

    def get(self, request, *args, **kwargs):
        """
        Redirect if unauthenticated user attempts to view private card.
        """
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        card = context['card']
        if card.private and not request.user.is_authenticated:
            return redirect(reverse('auth_extension:unauthorized'))
        else:
            return self.render_to_response(context)

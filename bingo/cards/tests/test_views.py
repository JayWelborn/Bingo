from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from cards.models import BingoCard, BingoCardSquare

import pdb


class CardListViewTests(TestCase):
    """Tests for CardListView class

    Methods:
        setUp: Create cards for testing
        test_template_used: View should use `cards/card_list.html`
            and return 200
        test_context_object_name: List of cards should be in
            context['bingocards']
        test_cards_sorted_correctly: Cards should be sorted most recent first
        test_cards_filtered_by_privacy: Private cards should only disply for
            authenticated users
        test_authenticated_user_can_see_private_cards: Authenticated users
            should be able to see private cards in list.

    References:
        * https://www.obeythetestinggoat.com/book/appendix_Django_Class-Based_Views.html

    """

    def setUp(self):
        """
        Create objects for testing
        """

        # Create User
        self.user = User.objects.create(
            username='cardviewtests',
            email='cardviewtest@gmail.com'
        )
        self.user.set_password('c@RdviewTe5t5')
        self.user.save()

        self.assertTrue(self.user)

        # Create bingocards
        self.cards = []
        self.private_cards = []

        for i in range(10):
            # Public Cards
            card = BingoCard.objects.create(
                title='card # {}'.format(i),
                created_date=timezone.now() - timedelta(days=i),
                creator=self.user,
            )
            card.save()
            self.cards.append(card)

            # Private Cards
            private_card = BingoCard.objects.create(
                title='card # {}'.format(i),
                created_date=timezone.now() - timedelta(days=i),
                creator=self.user,
                private=True
            )
            private_card.save()
            self.private_cards.append(private_card)

        self.assertEqual(len(self.cards), 10)
        self.assertEqual(len(self.private_cards), 10)

        for card in self.private_cards:
            self.assertTrue(card.private)

        for card in self.cards:
            self.assertFalse(card.private)

    def test_template_used(self):
        """
        View shoud use `cards/card_list.html`.
        """

        response = self.client.get(reverse('cards:card_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            'cards/card_list.html'
        )

    def test_context_object_name(self):
        """
        View should render with cards stored in context['bingocards'].
        """

        response = self.client.get(reverse('cards:card_list'))
        self.assertIn('bingocards', response.context)

    def test_cards_sorted_correctly(self):
        """
        Cards should be sorted by date.
        """

        response = self.client.get(reverse('cards:card_list'))
        self.assertEqual(response.status_code, 200)
        cards = response.context['bingocards']

        for i in range(1, len(cards)):
            current = cards[1]
            previous = cards[0]
            self.assertTrue(current.created_date < previous.created_date)

    def test_cards_filtered_by_privacy(self):
        """
        Private cards should not display for unauthenticated visitors
        """

        self.client.logout()

        response = self.client.get(reverse('cards:card_list'))
        cards = response.context['bingocards']
        for card in cards:
            self.assertFalse(card.private)

    def test_authenticated_user_can_see_private_cards(self):
        """
        Authenticated Users should be able to see private cards.
        """

        self.client.login(
            username='cardviewtests',
            password='c@RdviewTe5t5'
        )

        # Ensure user is logged in
        self.assertIn('_auth_user_id', self.client.session)

        response = self.client.get(reverse('cards:card_list'))
        cards = list(response.context['bingocards'])

        for index, card in enumerate(cards):
            if not card.private:
                cards.pop(index)

        self.assertTrue(cards)
        for card in cards:
            self.assertTrue(card.private)

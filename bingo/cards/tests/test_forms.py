from django.contrib.auth.models import User
from django.test import TestCase

from cards.forms import BingoCardForm, BingoSquareForm
from cards.models import BingoCard, BingoCardSquare

import pdb


class BingoCardFormtests(TestCase):
    """Tests for BingoCardForm

    Methods:
        setUp: Create test data for form
        test_helper: Crispy helper should exist and have appropriate attributes
        test_form_accepts_valid_data: Form should accept valid data
        test_card_created_correctly: New BingoCard should be created with data
            from form, and defaults for attributes not included in the form.

    References:

    * http://test-driven-django-development.readthedocs.io/en/latest/05-forms.html

    """

    def setUp(self):
        """
        Create Test data.
        """

        # User to serve as card's creator
        self.user = User.objects.create(
            username='CardFormTestUser',
            email='formtest@gmail.com'
        )
        self.user.set_password('cardf0rm!')
        self.user.save()

        # sample form data
        self.data = {
            'title': 'FormTestTitle',
            'free_space': 'FormTestFreeSpace',
            'creator': str(self.user.id),
            'private': False
        }

    def test_helper(self):
        """
        Form should get crispy helper attributes when instantiated.
        """

        form = BingoCardForm()

        self.assertTrue(form.helper)
        self.assertEqual(form.helper.form_id, 'bingo_card_form')
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.form_action, '.')

    def test_form_accepts_valid_data(self):
        """
        Form should accept and process valid data.
        """
        form = BingoCardForm(self.data)

        self.assertTrue(form.is_valid())

    def test_card_created_correctly(self):
        """
        Form should create new BingoCard properly.
        """

        # instantiate form, and save it
        form = BingoCardForm(self.data)
        if form.is_valid():
            test_card = form.save()

        # check card in DB against card returned by form
        card = BingoCard.objects.get(title='FormTestTitle')
        self.assertTrue(card)
        self.assertEqual(card, test_card)
        self.assertEqual(card.creator, self.user)


class BingoSquareFormtests(TestCase):
    """Tests for BingoCardForm

    Methods:
        setUp: Create test data for form
        test_helper: Crispy helper should exist and have appropriate attributes
        test_form_accepts_valid_data: Form should accept valid data
        test_card_created_correctly: New BingoSquare should be created with
        data from form, and defaults for attributes not included in the form.

    References:

    * http://test-driven-django-development.readthedocs.io/en/latest/05-forms.html

    """

    def setUp(self):
        """
        Create Test data.
        """

        # User to serve as card's creator
        self.user = User.objects.create(
            username='CardSquareTestUser',
            email='squaretest@gmail.com'
        )
        self.user.set_password('squaref0rm!')
        self.user.save()

        self.card = BingoCard.objects.get_or_create(
            title='SquareFormTest',
            creator=self.user,
        )[0]
        self.card.save()

        self.data = {
            'text': 'CardSquareTest',
            'card': str(self.card.id),
        }

    def test_helper(self):
        """
        Form should get crispy helper attributes when instantiated.
        """

        form = BingoSquareForm()

        self.assertTrue(form.helper)
        self.assertEqual(form.helper.form_id, 'bingo_square_form')
        self.assertEqual(form.helper.form_method, 'post')
        self.assertEqual(form.helper.form_action, '.')

    def test_form_accepts_valid_data(self):
        """
        Form should accept and process valid data.
        """
        form = BingoSquareForm(self.data)
        self.assertTrue(form.is_valid())

    def test_square_created_correctly(self):
        """
        Form should create new BingoCard properly.
        """

        # instantiate form, and save it
        form = BingoSquareForm(self.data)
        if form.is_valid():
            test_square = form.save()

        # check card in DB against card returned by form
        square = BingoCardSquare.objects.get(text='CardSquareTest')
        self.assertTrue(square)
        self.assertEqual(square, test_square)
        self.assertEqual(square.card, self.card)
        self.assertEqual(square.card.creator, self.user)

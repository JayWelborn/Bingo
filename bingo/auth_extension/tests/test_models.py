from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.test import TestCase
from django.urls import reverse

# Create your tests here.
from auth_extension.models import UserProfile


class UserProfileModelTests(TestCase):
    """Tests for Contact Model

    Methods:
        setUp: Creates sample UserProfile object for testing
        test_profile_links_to_user: Ensures User and UserProfile objects are
            linked as expected
        test_slugify_for_user_profile: Ensures username is correctly slugified
            when UserProfile instance is saved
        test_get_absolute_url: define url for viewing object instances

    References:
        * https://docs.djangoproject.com/en/1.11/topics/testing/

    """

    def setUp(self):
        """
        Create instance(s) for tests
        """
        self.test_user_one = User.objects.create(username='test one',
                                                 password='password',
                                                 email='test@test.com',)

        self.test_user_two = User.objects.create(username='test two',
                                                 password='password1',
                                                 email='test2@test.com')

        self.test_profile = UserProfile.objects.create(user=self.test_user_one)

    def test_profile_links_to_user(self):
        """
        Test to ensure UserProfile object is linked to a User upon creation
        """
        self.assertEqual(self.test_profile.user, self.test_user_one)
        self.assertEqual(self.test_user_one.profile, self.test_profile)

    def test_slugify_for_user_profile(self):
        """
        Test to ensure username slug is stored as expected when UserProfile
        instance is created
        """
        test_slug = slugify(self.test_user_one.username)
        self.assertEqual(self.test_profile.slug, test_slug)
        self.assertEqual(self.test_profile.slug, 'test-one')

    def test_get_absolute_url(self):
        """
        Absolute url should match the regex pattern from app-level urlconf
        """
        pk = self.test_profile.pk
        reversed_url = reverse('auth_extension:profile', args=[pk])
        expected_url = '/profile/{}/'.format(pk)
        self.assertEqual(reversed_url, expected_url)
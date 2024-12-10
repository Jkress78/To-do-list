from django.test import TestCase, Client
from django.utils import timezone
from django.urls import reverse
from django.http import HttpRequest

from .models import List, ListItem, User
# Create your tests here.

class DashboardViewTests(TestCase):
    def test_no_lists(self):
        u = User.objects.create(email="jim@jim.ca", pswd="abc123", name_first="jim",
                                name_last="Jim", prof_img="")
        url = reverse("todo:listSelect", args=(u.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have no existing lists")

    def test_one_or_more_lists(self):
        u = User.objects.create(email="jim@jim.ca", pswd="abc123", name_first="jim",
                                name_last="Jim", prof_img="")
        u.save()
        l = List.objects.create(user=u, list_name="jim's list", 
                                create_date=timezone.now(), cover_img="static\images\paper_s.png")
        
        l.save()

        url = reverse("todo:listSelect", args=(u.id,))
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
        
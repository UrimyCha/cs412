from django.db import models
from django.urls import reverse

# Create your models here.
class Profile(models.Model):
    # first name, last name, city, email address, and a profile image url.
    firstname = models.TextField(blank=False)
    lastname = models.TextField(blank=False)
    city = models.TextField(blank=False)
    email = models.TextField(blank=False)
    image_url = models.URLField(blank=False)

    def __str__(self):
        return f'{self.firstname} {self.lastname}'
    
    def get_status_messages(self):
        '''Retrieve all comments for this article'''

        # use the ORM to filter comments where this instance of Article is the FK
        message = StatusMessage.objects.filter(profile=self)     # could have used pk of this object or just self
        return message
    
    def get_absolute_url(self):
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_friends(self):
        friend1 = Friend.objects.filter(profile1=self) 
        friend2 = Friend.objects.filter(profile2=self) 

        friends_profiles = [friend.profile2 for friend in friend1] + [friend.profile1 for friend in friend2]

        return friends_profiles
    
    def add_friend(self,other):
        # Ensure self-friending is not allowed
        if self == other:
            raise ValueError("A profile cannot friend itself.")
        
        # Check if the friend relationship already exists in either direction
        existing_friendship = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists()

        # If no existing friendship is found, create a new Friend instance
        if not existing_friendship:
            new_friendship = Friend(profile1=self, profile2=other)
            new_friendship.save()

    def get_friend_suggestions(self):
        # Get IDs of profiles that are already friends with this profile
        friend_ids = Friend.objects.filter(
            models.Q(profile1=self) | models.Q(profile2=self)
        ).values_list('profile1__id', 'profile2__id')
        
        # Flatten the list of friend IDs and remove duplicates
        friend_ids = {id for ids in friend_ids for id in ids if id != self.id}
        
        # Get all profiles excluding the current profile and its friends
        suggestions = Profile.objects.exclude(id__in=friend_ids).exclude(id=self.id)
        
        return suggestions
    
    def get_news_feed(self):
        friend_ids = Friend.objects.filter(
            models.Q(profile1=self) | models.Q(profile2=self)
        ).values_list('profile1__id', 'profile2__id')

        friend_ids = {id for ids in friend_ids for id in ids}

        newsfeed = StatusMessage.objects.filter(profile__id__in=friend_ids).order_by('-timestamp')

        return newsfeed


class StatusMessage(models.Model):
    # model the data attributes of Facebook status message
    timestamp = models.DateTimeField(auto_now=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey("Profile", on_delete=models.CASCADE)

    def __str__(self):
        """Return a string representation of this object"""
        return f'{self.message}'
    
    def get_images(self):
        """ Return all images associated with this status message """
        image = Image.objects.filter(status_message=self)    
        return image

class Image(models.Model):
    # model for uploading image files to a status message
    timestamp = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True)
    status_message = models.ForeignKey("StatusMessage", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.image}'

class Friend(models.Model):
    profile1 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey("Profile", on_delete=models.CASCADE, related_name="profile2")
    anniversary = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.profile1.firstname} {self.profile1.lastname} & {self.profile2.firstname} {self.profile2.lastname}'








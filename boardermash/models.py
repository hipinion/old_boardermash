from django.db import models

class Boarder(models.Model):
    def __unicode__(self):
	return self.fname
    
    def hasAvatar(self):
	if self.avatar_link <> "":
	    return True
	else:
	    return False

    fname = models.CharField(max_length=200)
    dname = models.CharField(max_length=400)
    num_posts = models.IntegerField()
    avatar_link = models.CharField(max_length=1000, null=True, blank=True)
    avatar_height = models.IntegerField(null=True, blank=True)
    avatar_width = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    score = models.IntegerField()

class MashSession(models.Model):
    def __unicode__(self):
	return self.username + " " + str(self.start_time)

    username = models.CharField(max_length=200)
    validated = models.BooleanField()
    key_phrase = models.CharField(max_length=1000)
    start_time = models.DateTimeField('Session Start Time')
    stop_time = models.DateTimeField('Session Stop Time', null=True, blank=True)


class Mash(models.Model):
    def __unicode__(self):
	return " v.s. ".join([str(b) for b in self.boarders.all()])
    
    boarders = models.ManyToManyField(Boarder)
    mash_datetime = models.DateTimeField('Mash time')
    winner_fname = models.CharField(max_length=200, null=True, blank=True)
    mash_session = models.ForeignKey(MashSession) 


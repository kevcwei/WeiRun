from django.db import models


class User(models.Model):
    """Nike+ user model."""

    id = models.CharField(max_length=50, primary_key=True)
    screen_name = models.CharField(max_length=50, db_index=True)
    distance = models.FloatField()
    distance_unit = models.CharField(max_length=2)
    plus_level = models.IntegerField()

    def distance_in_preferred_unit(self):
        """Convert the default distance in km to distance in user preferred unit.

        Returns:
            A float of distance.
        """
        if self.distance_unit == 'km':
            return self.distance
        else:
            return self.distance * 0.621371192

    def __unicode__(self):
        """Converts the instance to a string.

        Returns:
            A string of the user's info.
        """
        return u'%s (Level %d)' % (self.screen_name, self.plus_level)


class Run(models.Model):
    """Nike+ run model."""

    id = models.IntegerField(primary_key=True)
    start_time = models.DateTimeField()
    duration = models.IntegerField()
    distance = models.FloatField()
    calories = models.FloatField()
    user = models.ForeignKey('User')
    
    def url(self):
        """Constructs a url of this run.

        Returns:
            A string of the url.
        """
        return 'http://nikerunning.nike.com/nikeplus/v2/services/dashboard/og_run.jsp?activityid=%d&namespace=nikeapp&locale=zh_CN' % self.id

    def __unicode__(self):
        """Converts the instance to a string.

        Returns:
            A string of the run.
        """
        return u'%s %d' % (self.user.screen_name, self.distance)
    

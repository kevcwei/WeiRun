import urllib2
from lxml import etree


class User:
    """A class that wraps user's info."""

    def __init__(self, id, screen_name, distance_unit, total_distance, plus_level):
        """User constructor.

        Args:
            screen_name: The name displays on Nike+ website.
            distance_unit: Can be either mi or km.
            total_distance: Total distance in kilos.
            plus_level: 0-based Nike+ level. Find more on http://bit.ly/12c47y. 
        """
        self.id = id
        self.screen_name = screen_name
        self.distance_unit = distance_unit
        self.plus_level = plus_level
        self._total_distance = total_distance
        if self.distance_unit == 'km':
            self.distance = self._total_distance
        else:
            self.distance = self._total_distance * 0.621371192        

    def __str__(self):
        """Converts the instance to a string.

        Returns:
            A pretty string of the user's info.
        """
        return "%s (Level %d) %.2f%s" % (self.screen_name,
                                         self.plus_level,
                                         self.distance,
                                         self.distance_unit)


class Nike:
    """Grab runs from Nike."""
    
    def __init__(self, id):
        """Nike constructor.
        
        Args:
            id: Nike+ user id. See readme for determing this.
        """
        self.id = id

    def runs(self):
        """Parsers runs XML file and extracts runs info.

        Returns:
            A list of instances of Run class.
        """ 
        pass

    def user(self):
        """Parsers user XML file and extracts useful info.

        Returns:
            A instance of User class.
        """ 
        tree = etree.fromstring(self._get_user_xml())
        screen_name = tree.xpath('/plusService/userOptions/screenName/text()')
        if screen_name:
            screen_name = screen_name[0]
        distance_unit = tree.xpath('/plusService/userOptions/distanceUnit/text()')
        if distance_unit:
            distance_unit = distance_unit[0]
        total_distance = tree.xpath('/plusService/userTotals/totalDistance/text()')
        if total_distance:
            total_distance = float(total_distance[0])
        plus_level = tree.xpath('/plusService/user/plusLevel/text()')
        if plus_level:
            plus_level = int(plus_level[0])
        return User(self.id, screen_name, distance_unit, total_distance, plus_level)

    def _get_runs_xml(self):
        """Retrieves a list of runs in XML.

        Returns:
            A string of the XML content.
        """
        url = 'http://nikerunning.nike.com/nikeplus/v1/services/widget/get_public_run_list.jsp?userID=' + self.id
        f = urllib2.urlopen(url)
        xml = f.read()
        f.close()
        return xml

    def _get_user_xml(self):
        """Retrieves user's info in XML.

        Returns:
            A string of the XML content.
        """
        url = 'http://nikerunning.nike.com/nikeplus/v1/services/widget/get_public_user_data.jsp?userID=' + self.id 
        f = urllib2.urlopen(url)
        xml = f.read()
        f.close()
        return xml

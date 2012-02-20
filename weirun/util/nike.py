import urllib2
from lxml import etree
from main.models import User, Run


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
            A instance of User class. If fails to get user info, returns None.
        """ 
        tree = etree.fromstring(self._get_user_xml())
        status = tree.xpath('/plusService/status/text()')
        if not status or status[0] == 'failure':
            return None
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
        return User(id=self.id, screen_name=screen_name, distance=total_distance,
                    distance_unit=distance_unit, plus_level=plus_level)

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

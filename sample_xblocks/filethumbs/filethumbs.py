"""An XBlock providing thumbs-up/thumbs-down voting."""

from xblock.core import XBlock
from xblock.fields import Scope, Integer, Boolean, Filesystem
from xblock.fragment import Fragment
import pkg_resources

import logging
log = logging.getLogger(__name__)


class FileThumbsBlock(XBlock):
    """
    An XBlock with thumbs-up/thumbs-down voting.

    Vote totals are stored for all students to see.  Each student is recorded
    as has-voted or not.

    This demonstrates multiple data scopes and ajax handlers.

    """

    upvotes = Integer(help="Number of up votes", default=0, scope=Scope.user_state_summary)
    downvotes = Integer(help="Number of down votes", default=0, scope=Scope.user_state_summary)
    voted = Boolean(help="Has this student voted?", default=False, scope=Scope.user_state)
    fs = Filesystem(help="File system", scope=Scope.user_state)

    def student_view(self, context=None):  # pylint: disable=W0613
        """
        Create a fragment used to display the XBlock to a student.
        `context` is a dictionary used to configure the display (unused)

        Returns a `Fragment` object specifying the HTML, CSS, and JavaScript
        to display.
        """

        # Load the HTML fragment from within the package and fill in the template
        html_str = pkg_resources.resource_string(__name__, "static/html/thumbs.html")
        frag = Fragment(unicode(html_str).format(self=self))

        # Load the CSS and JavaScript fragments from within the package
        css_str = pkg_resources.resource_string(__name__, "static/css/thumbs.css")
        frag.add_css(unicode(css_str))

        js_str = pkg_resources.resource_string(__name__,
                                               "static/js/src/thumbs.js")
        frag.add_javascript(unicode(js_str))

        self.fs.open("hello.txt")

        frag.initialize_js('FileThumbsBlock')
        return frag

    problem_view = student_view

    @XBlock.json_handler
    def vote(self, data, suffix=''):  # pylint: disable=unused-argument
        """
        Update the vote count in response to a user action.
        """
        # Here is where we would prevent a student from voting twice, but then
        # we couldn't click more than once in the demo!
        #
        #     if self.voted:
        #         log.error("cheater!")
        #         return

        if data['voteType'] not in ('up', 'down'):
            log.error('error!')
            return

        if data['voteType'] == 'up':
            self.upvotes += 1
        else:
            self.downvotes += 1

        self.voted = True

        return {'up': self.upvotes, 'down': self.downvotes}

    @staticmethod
    def workbench_scenarios():
        """A canned scenario for display in the workbench."""
        return [
            ("filethumbs",
             """\
                <vertical_demo>
                    <filethumbs/>
                    <filethumbs/>
                    <filethumbs/>
                </vertical_demo>
             """)
        ]

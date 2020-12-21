from django.template import Library, Node, NodeList
from django.template.defaulttags import CycleNode
from django.template.base import TemplateSyntaxError
from django.utils.safestring import SafeString

register = Library()


class Multiplier(Node):
    def __init__(self, nodelist, ratio):
        self.nodelist = nodelist
        self.ratio = ratio

    def render(self, context):
        content = ''
        for _ in range(self.ratio):
            content += self.nodelist.render(context)
        return content


@register.tag
def multiply(parser, token):
    bits = token.split_contents()
    ratio = int(bits[1])
    nodelist = parser.parse(('endmultiply', None))
    parser.next_token()
    return Multiplier(nodelist, ratio)


@register.tag(name='range')
def do_range(parser, token):
    args = token.split_contents()

    as_form = False
    if len(args) > 3:
        # {% cycle ... as foo [silent] %} case.
        if args[-3] == "as":
            if args[-1] != "silent":
                raise TemplateSyntaxError("Only 'silent' flag is allowed after range cycle's name, not '%s'." % args[-1])
            as_form = True
            silent = True
            args = args[:-1]
        elif args[-2] == "as":
            as_form = True
            silent = False

    if as_form:
        name = args[-1]
        values = [parser.compile_filter(arg) for arg in args[1:-2]]
        node = CycleNode(values, name, silent=silent)
        if not hasattr(parser, '_named_cycle_nodes'):
            parser._named_cycle_nodes = {}
        parser._named_cycle_nodes[name] = node
    elif len(args) < 5:
        values = [parser.compile_filter(str(arg)) for arg in range(*[int(arg) for arg in args[1:]])]
        node = CycleNode(values)
    else:
        raise TemplateSyntaxError('Range allowed only 3 args: (start, stop, step)')

    return node

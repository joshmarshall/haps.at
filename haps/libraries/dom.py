""" A few DOM utilities. """

def get_text(element):
    """ Extracts the text from a single element node """
    results = []
    for node in element.childNodes:
        if node.nodeType == node.TEXT_NODE:
            results.append(node.data)
    return ''.join(results)

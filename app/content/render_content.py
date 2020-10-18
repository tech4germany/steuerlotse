from flask import render_template
from flask_babel import _


def render_how_it_works():
    accordeon = {
        'one': {
            'heading': _('howitworks.card-1.heading'),
            'paragraphs': [
                (_('howitworks.card-1.p1-desc'), _('howitworks.card-1.p1-content')),
                (_('howitworks.card-1.p2-desc'), _('howitworks.card-1.p2-content')),
                (_('howitworks.card-1.p3-desc'), _('howitworks.card-1.p3-content')),
            ],
            'list-items': [
                _('howitworks.card-1.list-item-1'),
                _('howitworks.card-1.list-item-2'),
                _('howitworks.card-1.list-item-3'),
            ],
        },
        'two': {
            'heading': _('howitworks.card-2.heading'),
            'paragraphs': [
                (_('howitworks.card-2.p1-desc'), _('howitworks.card-2.p1-content')),
                (_('howitworks.card-2.p2-desc'), _('howitworks.card-2.p2-content')),
                (_('howitworks.card-2.p3-desc'), _('howitworks.card-2.p3-content')),
            ],
            'list-items': None,
        },
        'three': {
            'heading': _('howitworks.card-3.heading'),
            'paragraphs': [
                (_('howitworks.card-3.p1-desc'), _('howitworks.card-3.p1-content')),
                (_('howitworks.card-3.p2-desc'), _('howitworks.card-3.p2-content')),
                (_('howitworks.card-3.p3-desc'), _('howitworks.card-3.p3-content')),
            ],
            'list-items': None,
        },
        'four': {
            'heading': _('howitworks.card-4.heading'),
            'paragraphs': [
                (_('howitworks.card-4.p1-desc'), _('howitworks.card-4.p1-content')),
                (_('howitworks.card-4.p2-desc'), _('howitworks.card-4.p2-content')),
                (_('howitworks.card-4.p3-desc'), _('howitworks.card-4.p3-content')),
            ],
            'list-items': None,
        },
    }
    return render_template('content/howitworks.html', accordeon=accordeon)

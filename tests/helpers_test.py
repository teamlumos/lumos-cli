
from common.helpers import get_statuses
from common.models import SupportRequestStatus


def test_get_statuses():
    assert get_statuses([], False, False) is None
    assert get_statuses(None, False, False) is None

def test_get_statuses_just_pending():
    assert get_statuses([SupportRequestStatus.PENDING], False, False) == set([SupportRequestStatus.PENDING])
    assert get_statuses([SupportRequestStatus.PENDING], True, False) == set(SupportRequestStatus.PENDING_STATUSES)
    assert get_statuses([], True, False) == set(SupportRequestStatus.PENDING_STATUSES)

def test_get_statusees_pending_and_past():
    not_pending = set(SupportRequestStatus.ALL_STATUSES).difference(set(SupportRequestStatus.PENDING_STATUSES))
    not_pending.add(SupportRequestStatus.PENDING)
    assert get_statuses([SupportRequestStatus.PENDING], False, True) == not_pending
    assert get_statuses([SupportRequestStatus.PENDING], True, True) == set(SupportRequestStatus.ALL_STATUSES)

    pending_and_completed = set(SupportRequestStatus.PENDING_STATUSES)
    pending_and_completed.add(SupportRequestStatus.COMPLETED)
    assert get_statuses([SupportRequestStatus.COMPLETED], True, False) == pending_and_completed

def test_get_statuses_all_statuses():
    assert get_statuses([], True, True) == set(SupportRequestStatus.ALL_STATUSES)

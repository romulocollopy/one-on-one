import rules


@rules.predicate
def is_in_relation(boby, relation):
    if boby in (relation.inviter, relation.invited):
        return True
    return False


@rules.predicate
def is_admin(boby):
    return boby.is_staff or boby.is_superuser

rules.add_rule('can_change_bobyrelation', is_in_relation | is_admin)

rules.add_perm('core.change_bobyrelation', is_in_relation | is_admin)

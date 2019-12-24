def menu_tree_to_vue(menus):
    res = []
    for menu in menus:
        tmp = {
            'id': menu.id,
            'name': menu.name,
            'path': menu.path,
            'component': menu.component,
            'hidden': menu.is_show is False,
            'meta': {
                'title': menu.title,
                'icon': menu.icon,
                'no_cache': menu.is_cache is False,
                'roles': [role.slug for role in menu.roles.all()]
            }
        }
        if hasattr(menu, 'children'):
            tmp['children'] = menu_tree_to_vue(menu.children)

        res.append(tmp)
    return res


class PermInspector(object):
    """
    权限判断
    """

    SUPER_ADMIN_IDS = [1]

    def is_super_admin(self, user):
        if not user:
            return False

        if user.id in self.SUPER_ADMIN_IDS:
            return True

        if not user.role_slugs:
            return False

        if 'super_admin' in user.role_slugs:
            return True

        return False

    def check_role(self, user, role_slugs):
        """
        检查用户角色
        :param user:
        :param role_slugs:
        :return:
        """

        if self.is_super_admin(user):
            return True

        if not role_slugs:
            return True

        user_role_slugs = user.role_slugs
        if not user_role_slugs:
            return False

        inter_slugs = list(set(user_role_slugs) & set(role_slugs))
        if inter_slugs:
            return True

        return False


perm_inspector = PermInspector()

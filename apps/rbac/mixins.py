from django.contrib.auth.models import PermissionsMixin
from django.db import models


class ModelTreeMixin(models.Model):
    """
    自定义 Tree
    """

    def get_manager(self):
        return self._meta.base_manager

    def get_parent_field(self):
        raise NotImplementedError('`get_parent_field()` must be implemented.')

    def get_order_field(self):
        return ''

    def to_tree(self):
        return self.build_nested_list()

    def ignore_tree_node(self, node):
        return False

    def build_nested_list(self, nodes=None, parent_id=None):
        branch = []
        parent_field = self.get_parent_field()
        if nodes is None:
            nodes = self.all_nodes()

        for node in nodes:
            if self.ignore_tree_node(node):
                continue
            if getattr(node, parent_field) == parent_id:
                children = self.build_nested_list(nodes, node.id)
                setattr(node, 'children', children)
                branch.append(node)
        return branch

    def all_nodes(self):
        order_fields = self.get_order_field()
        if order_fields:
            nodes = self.get_manager().order_by(order_fields)
        else:
            nodes = self.get_manager().all()

        return nodes

    class Meta:
        abstract = True

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:owefsad
# datetime:2021/3/9 下午12:06
# software: PyCharm
# project: lingzhi-engine
import logging

from dongtai.models.hook_strategy import HookStrategy

from dongtai.utils import const
from dongtai.endpoint import R, UserEndPoint

logger = logging.getLogger('dongtai-engine')


class HookRuleTypeEnableEndPoint(UserEndPoint):
    def parse_args(self, request):
        try:
            rule_id = request.query_params.get('rule_id', const.RULE_PROPAGATOR)
            rule_type = int(rule_id)
            return rule_type
        except Exception as e:
            logger.error(f"参数处理失败，错误详情：{e}")
            return None

    def get(self, request):
        rule_id = self.parse_args(request)
        if rule_id is None:
            return R.failure(msg='策略不存在')

        rule = HookStrategy.objects.filter(id=rule_id, created_by=request.user.id).first()
        if rule:
            rule_type = rule.type.first()
            if rule_type:
                rule_type.enable = const.ENABLE
                rule.save()
                return R.success(msg='启用成功')
        return R.failure(msg='策略类型不存在')

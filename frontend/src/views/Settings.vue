<template>
  <div class="grid min-h-[calc(100vh-120px)] grid-cols-12 gap-4">
    <div class="col-span-12 xl:col-span-3">
      <GlassCard title="成果与参数中心" class="h-full">
        <div class="space-y-4">
          <div class="space-y-1">
            <button
              v-for="item in menuItems"
              :key="item.key"
              @click="activeTab = item.key"
              class="flex w-full items-center gap-3 rounded-xl border px-3 py-3 text-left transition-all"
              :class="activeTab === item.key ? 'border-cyber-neonViolet/40 bg-cyber-neonViolet/10 text-slate-100' : 'border-white/10 bg-white/5 text-slate-400 hover:border-cyber-neonViolet/20 hover:bg-white/8'"
            >
              <span class="flex h-9 w-9 items-center justify-center rounded-lg bg-white/5 text-lg">{{ item.icon }}</span>
              <div class="min-w-0">
                <div class="text-sm font-medium">{{ item.label }}</div>
                <div class="text-[10px] text-slate-500">{{ item.hint }}</div>
              </div>
            </button>
          </div>

          <div class="rounded-xl border border-cyber-neonCyan/15 bg-cyber-neonCyan/5 p-4">
            <div class="mb-3 flex items-center gap-3">
              <div class="flex h-10 w-10 items-center justify-center rounded-full bg-cyber-neonViolet/20 text-sm">
                {{ userRoleIcon }}
              </div>
              <div>
                <div class="text-sm font-medium text-slate-100">{{ authStore.user?.username || '未登录' }}</div>
                <div class="text-[11px] text-slate-400">{{ userRoleText }}</div>
              </div>
            </div>
            <div class="space-y-2 text-xs">
              <div class="flex items-center justify-between">
                <span class="text-slate-400">权限级别</span>
                <span class="text-cyber-neonCyan">{{ userPermissions }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-400">当前口径</span>
                <span class="text-cyber-neonViolet">比赛展示版</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-400">重点对象</span>
                <span class="text-slate-300">{{ activeGreenhouse.name }}</span>
              </div>
            </div>
          </div>

          <div class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 text-sm font-medium text-slate-100">页面说明</div>
            <div class="text-xs leading-6 text-slate-400">
              本页已从传统“后台设置”调整为“比赛展示型成果中心”，突出参数边界、阶段成果、数据口径与可复制推广逻辑。
            </div>
          </div>
        </div>
      </GlassCard>
    </div>

    <div class="col-span-12 xl:col-span-9 space-y-4">
      <template v-if="activeTab === 'overview'">
        <div class="grid gap-4 md:grid-cols-2 2xl:grid-cols-4">
          <div v-for="stat in overviewStats" :key="stat.key" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center justify-between">
              <div class="flex items-center gap-2">
                <span class="text-lg">{{ stat.icon }}</span>
                <span class="text-xs text-slate-400">{{ stat.label }}</span>
              </div>
              <span class="rounded-full px-2 py-1 text-[10px]" :class="stat.badgeClass">{{ stat.badge }}</span>
            </div>
            <div class="text-2xl font-semibold" :class="stat.color">{{ stat.value }}</div>
            <div class="mt-1 text-[11px] text-slate-500">{{ stat.trend }}</div>
          </div>
        </div>

        <div class="grid grid-cols-12 gap-4">
          <GlassCard title="多棚环境指标对比" class="col-span-12 2xl:col-span-6">
            <template #right>
              <div class="flex items-center gap-2">
                <select v-model="compareGreenhouse1" class="rounded border border-white/10 bg-white/5 px-2 py-1 text-[10px]">
                  <option v-for="g in greenhouses" :key="g.id" :value="g.id">{{ g.name }}</option>
                </select>
                <span class="text-slate-500">vs</span>
                <select v-model="compareGreenhouse2" class="rounded border border-white/10 bg-white/5 px-2 py-1 text-[10px]">
                  <option v-for="g in greenhouses" :key="g.id" :value="g.id">{{ g.name }}</option>
                </select>
              </div>
            </template>
            <div ref="radarChartEl" class="h-[300px]" />
          </GlassCard>

          <GlassCard title="7天关键参数趋势" class="col-span-12 2xl:col-span-6">
            <template #right>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="metric in trendMetrics"
                  :key="metric.key"
                  @click="activeTrendMetric = metric.key"
                  class="rounded-full px-2 py-1 text-[10px] transition-colors"
                  :class="activeTrendMetric === metric.key ? 'bg-cyber-neonViolet/20 text-cyber-neonViolet' : 'bg-white/5 text-slate-400'"
                >
                  {{ metric.label }}
                </button>
              </div>
            </template>
            <div ref="trendChartEl" class="h-[300px]" />
          </GlassCard>
        </div>

        <div class="grid grid-cols-12 gap-4">
          <GlassCard title="阶段成果模拟指标" class="col-span-12 xl:col-span-4">
            <div class="space-y-3">
              <div v-for="item in mockAchievements" :key="item.label" class="rounded-xl border border-white/10 bg-white/5 p-4">
                <div class="mb-2 flex items-center justify-between">
                  <div class="text-sm font-medium text-slate-100">{{ item.label }}</div>
                  <span class="text-xs" :class="item.trendClass">{{ item.trend }}</span>
                </div>
                <div class="flex items-end justify-between gap-3">
                  <div>
                    <div class="text-2xl font-semibold" :class="item.valueClass">{{ item.value }}</div>
                    <div class="mt-1 text-[11px] text-slate-500">{{ item.note }}</div>
                  </div>
                  <div class="w-24">
                    <div class="mb-1 flex justify-between text-[10px] text-slate-500">
                      <span>可信度</span>
                      <span>{{ item.progress }}%</span>
                    </div>
                    <div class="h-2 rounded-full bg-white/10">
                      <div class="h-2 rounded-full bg-gradient-to-r from-cyber-neonViolet to-cyber-neonCyan" :style="{ width: `${item.progress}%` }" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </GlassCard>

          <GlassCard title="棚群达标率排行" class="col-span-12 xl:col-span-4">
            <div class="space-y-3">
              <div v-for="(g, index) in greenhouseRankings" :key="g.id" class="rounded-xl border border-white/10 bg-white/5 p-3">
                <div class="mb-2 flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <span class="flex h-7 w-7 items-center justify-center rounded-full bg-white/5 text-xs">{{ index + 1 }}</span>
                    <span class="text-sm text-slate-200">{{ g.name }}</span>
                  </div>
                  <span class="text-sm font-medium" :class="getScoreColor(g.score)">{{ g.score }}%</span>
                </div>
                <div class="h-2 rounded-full bg-white/10">
                  <div class="h-2 rounded-full" :class="getScoreBar(g.score)" :style="{ width: `${g.score}%` }" />
                </div>
                <div class="mt-1 text-[10px] text-slate-500">{{ g.comment }}</div>
              </div>
            </div>
          </GlassCard>

          <GlassCard title="作物类型分布" class="col-span-12 xl:col-span-4">
            <div ref="pieChartEl" class="h-[220px]" />
            <div class="mt-3 grid grid-cols-2 gap-2 text-xs">
              <div v-for="crop in cropLegend" :key="crop.name" class="flex items-center gap-2 rounded bg-white/5 px-3 py-2">
                <span class="h-2.5 w-2.5 rounded-full" :style="{ backgroundColor: crop.color }" />
                <span class="text-slate-400">{{ crop.name }}</span>
                <span class="ml-auto text-slate-200">{{ crop.value }}</span>
              </div>
            </div>
          </GlassCard>
        </div>
      </template>

      <template v-else-if="activeTab === 'greenhouse'">
        <div class="grid grid-cols-12 gap-4">
          <GlassCard title="目标大棚与作物画像" class="col-span-12 2xl:col-span-4">
            <div class="space-y-3">
              <button
                v-for="g in greenhouses"
                :key="g.id"
                @click="selectedGreenhouse = g.id"
                class="w-full rounded-xl border p-3 text-left transition-all"
                :class="selectedGreenhouse === g.id ? 'border-cyber-neonViolet/40 bg-cyber-neonViolet/10' : 'border-white/10 bg-white/5 hover:border-cyber-neonViolet/20'"
              >
                <div class="flex items-center justify-between">
                  <div>
                    <div class="text-sm font-medium text-slate-100">{{ g.name }}</div>
                    <div class="text-[11px] text-slate-400">{{ g.crop }} · {{ g.area }}㎡</div>
                  </div>
                  <span class="rounded-full bg-white/5 px-2 py-1 text-[10px]" :class="getScoreColor(g.score)">达标 {{ g.score }}%</span>
                </div>
              </button>
            </div>
          </GlassCard>

          <GlassCard title="关键环境参数口径表" class="col-span-12 2xl:col-span-8">
            <div class="overflow-x-auto">
              <table class="w-full min-w-[720px] text-left text-xs">
                <thead>
                  <tr class="border-b border-white/10 text-slate-400">
                    <th class="px-3 py-3 font-medium">指标</th>
                    <th class="px-3 py-3 font-medium">目标区间</th>
                    <th class="px-3 py-3 font-medium">当前值</th>
                    <th class="px-3 py-3 font-medium">检测意义</th>
                    <th class="px-3 py-3 font-medium">调控策略</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="row in parameterTable" :key="row.name" class="border-b border-white/5">
                    <td class="px-3 py-3 text-slate-200">
                      <div class="flex items-center gap-2">
                        <span>{{ row.icon }}</span>
                        <span>{{ row.name }}</span>
                      </div>
                    </td>
                    <td class="px-3 py-3 text-cyber-neonCyan">{{ row.range }}</td>
                    <td class="px-3 py-3" :class="row.currentClass">{{ row.current }}</td>
                    <td class="px-3 py-3 text-slate-400">{{ row.meaning }}</td>
                    <td class="px-3 py-3 text-slate-300">{{ row.action }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </GlassCard>
        </div>

        <div class="grid grid-cols-12 gap-4">
          <GlassCard title="灌溉计划与执行逻辑" class="col-span-12 2xl:col-span-6">
            <div class="space-y-3">
              <div v-for="(schedule, index) in irrigationSchedules" :key="index" class="rounded-xl border border-white/10 bg-white/5 p-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-3">
                    <span class="text-xl">💧</span>
                    <div>
                      <div class="text-sm font-medium text-slate-100">{{ schedule.time }}</div>
                      <div class="text-[11px] text-slate-400">{{ schedule.duration }}分钟 · {{ schedule.frequency }}</div>
                    </div>
                  </div>
                  <span class="rounded-full px-2 py-1 text-[10px]" :class="schedule.enabled ? 'bg-cyber-neonCyan/15 text-cyber-neonCyan' : 'bg-white/10 text-slate-400'">
                    {{ schedule.enabled ? '已启用' : '待启用' }}
                  </span>
                </div>
                <div class="mt-2 text-xs text-slate-500">触发条件：{{ schedule.conditions }}</div>
              </div>
              <div class="rounded-xl border border-cyber-neonCyan/15 bg-cyber-neonCyan/5 p-4 text-xs text-slate-300">
                今日累计灌溉 {{ todayIrrigationMinutes }} 分钟，计划总量 {{ plannedIrrigationMinutes }} 分钟；建议答辩时用它说明“从经验灌溉到条件灌溉”的升级。
              </div>
            </div>
          </GlassCard>

          <GlassCard title="作物阶段目标与SOP口径" class="col-span-12 2xl:col-span-6">
            <div class="space-y-3">
              <div v-for="item in stageTargets" :key="item.stage" class="rounded-xl border border-white/10 bg-white/5 p-4">
                <div class="mb-2 flex items-center justify-between">
                  <div class="text-sm font-medium text-slate-100">{{ item.stage }}</div>
                  <span class="rounded-full bg-white/5 px-2 py-1 text-[10px] text-slate-400">{{ item.days }}</span>
                </div>
                <div class="grid grid-cols-2 gap-2 text-[11px] text-slate-400">
                  <div>温度：<span class="text-slate-200">{{ item.temp }}</span></div>
                  <div>湿度：<span class="text-slate-200">{{ item.humidity }}</span></div>
                  <div>CO₂：<span class="text-slate-200">{{ item.co2 }}</span></div>
                  <div>重点动作：<span class="text-slate-200">{{ item.focus }}</span></div>
                </div>
              </div>
            </div>
          </GlassCard>
        </div>
      </template>

      <template v-else-if="activeTab === 'alerts'">
        <div class="grid grid-cols-12 gap-4">
          <GlassCard title="告警规则矩阵" class="col-span-12 2xl:col-span-8">
            <div class="grid gap-3 md:grid-cols-2">
              <div v-for="(rule, index) in alertRules" :key="index" class="rounded-xl border border-white/10 bg-white/5 p-4">
                <div class="mb-3 flex items-start justify-between">
                  <div class="flex items-center gap-3">
                    <div class="flex h-10 w-10 items-center justify-center rounded-lg text-xl" :class="rule.enabled ? 'bg-cyber-neonViolet/20' : 'bg-white/5'">
                      {{ rule.icon }}
                    </div>
                    <div>
                      <div class="text-sm font-medium text-slate-100">{{ rule.name }}</div>
                      <div class="text-xs text-slate-400">{{ rule.description }}</div>
                    </div>
                  </div>
                  <span class="rounded-full px-2 py-1 text-[10px]" :class="rule.enabled ? 'bg-cyber-neonCyan/15 text-cyber-neonCyan' : 'bg-white/10 text-slate-400'">
                    {{ rule.enabled ? '启用中' : '未启用' }}
                  </span>
                </div>
                <div class="grid grid-cols-2 gap-2 text-xs">
                  <div class="rounded-lg bg-white/5 p-2">
                    <div class="text-slate-500">触发阈值</div>
                    <div class="mt-1 text-slate-200">{{ rule.threshold }}</div>
                  </div>
                  <div class="rounded-lg bg-white/5 p-2">
                    <div class="text-slate-500">持续时间</div>
                    <div class="mt-1 text-slate-200">{{ durationMap[rule.duration] }}</div>
                  </div>
                  <div class="col-span-2 rounded-lg bg-white/5 p-2">
                    <div class="text-slate-500">自动处理</div>
                    <div class="mt-1" :class="rule.autoAction ? 'text-cyber-neonCyan' : 'text-slate-400'">{{ rule.autoAction ? '启用自动处置链路' : '仅预警，不直接动作' }}</div>
                  </div>
                </div>
              </div>
            </div>
          </GlassCard>

          <GlassCard title="告警统计与通知策略" class="col-span-12 2xl:col-span-4">
            <div class="grid grid-cols-3 gap-2">
              <div class="rounded-xl border border-cyber-neonPink/20 bg-cyber-neonPink/10 p-3 text-center">
                <div class="text-lg font-semibold text-cyber-neonPink">{{ alertStats.critical }}</div>
                <div class="text-[10px] text-slate-400">紧急</div>
              </div>
              <div class="rounded-xl border border-cyber-neonViolet/20 bg-cyber-neonViolet/10 p-3 text-center">
                <div class="text-lg font-semibold text-cyber-neonViolet">{{ alertStats.warning }}</div>
                <div class="text-[10px] text-slate-400">预警</div>
              </div>
              <div class="rounded-xl border border-cyber-neonCyan/20 bg-cyber-neonCyan/10 p-3 text-center">
                <div class="text-lg font-semibold text-cyber-neonCyan">{{ alertStats.info }}</div>
                <div class="text-[10px] text-slate-400">提示</div>
              </div>
            </div>
            <div class="mt-4 space-y-2">
              <div v-for="type in alertTypes" :key="type.name" class="flex items-center justify-between rounded-lg bg-white/5 px-3 py-2 text-xs">
                <span class="text-slate-400">{{ type.name }}</span>
                <span :class="type.color">{{ type.count }}次</span>
              </div>
            </div>
            <div class="mt-4 rounded-xl border border-white/10 bg-white/5 p-4 text-xs">
              <div class="mb-2 text-sm font-medium text-slate-100">通知策略</div>
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-slate-400">短信通知</span>
                  <span :class="notificationSettings.sms ? 'text-cyber-neonCyan' : 'text-slate-500'">{{ notificationSettings.sms ? '已启用' : '关闭' }}</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-slate-400">邮件通知</span>
                  <span :class="notificationSettings.email ? 'text-cyber-neonCyan' : 'text-slate-500'">{{ notificationSettings.email ? '已启用' : '关闭' }}</span>
                </div>
                <div class="flex items-center justify-between">
                  <span class="text-slate-400">应用内通知</span>
                  <span :class="notificationSettings.app ? 'text-cyber-neonCyan' : 'text-slate-500'">{{ notificationSettings.app ? '已启用' : '关闭' }}</span>
                </div>
              </div>
            </div>
          </GlassCard>
        </div>
      </template>

      <template v-else-if="activeTab === 'logs'">
        <GlassCard title="操作记录与过程追溯">
          <div class="mb-4 grid gap-3 md:grid-cols-4">
            <select v-model="logFilter.type" class="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs">
              <option value="">全部类型</option>
              <option value="control">设备控制</option>
              <option value="config">配置修改</option>
              <option value="alert">告警处理</option>
              <option value="login">登录注销</option>
            </select>
            <select v-model="logFilter.user" class="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs">
              <option value="">全部角色</option>
              <option value="admin">管理员</option>
              <option value="operator">操作员</option>
              <option value="viewer">观察员</option>
            </select>
            <input v-model="logFilter.search" type="text" placeholder="搜索操作内容..." class="rounded-xl border border-white/10 bg-white/5 px-3 py-2 text-xs" />
            <button @click="exportLogs" class="rounded-xl border border-cyber-neonViolet/20 bg-cyber-neonViolet/10 px-3 py-2 text-xs text-cyber-neonViolet transition-colors hover:bg-cyber-neonViolet/20">
              📥 导出记录
            </button>
          </div>

          <div class="overflow-auto rounded-xl border border-white/10">
            <table class="w-full min-w-[860px] text-left text-xs">
              <thead class="bg-white/5 text-slate-400">
                <tr>
                  <th class="px-3 py-3 font-medium">时间</th>
                  <th class="px-3 py-3 font-medium">用户</th>
                  <th class="px-3 py-3 font-medium">类型</th>
                  <th class="px-3 py-3 font-medium">操作内容</th>
                  <th class="px-3 py-3 font-medium">目标对象</th>
                  <th class="px-3 py-3 font-medium">结果</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="log in filteredLogs" :key="log.id" class="border-t border-white/5">
                  <td class="px-3 py-3 text-slate-400">{{ log.time }}</td>
                  <td class="px-3 py-3 text-slate-200">{{ log.username }}</td>
                  <td class="px-3 py-3">
                    <span class="rounded-full px-2 py-1 text-[10px]" :class="logTypeClass(log.type)">{{ log.typeText }}</span>
                  </td>
                  <td class="px-3 py-3 text-slate-300">{{ log.action }}</td>
                  <td class="px-3 py-3 text-slate-400">{{ log.greenhouse || '-' }}</td>
                  <td class="px-3 py-3" :class="log.success ? 'text-cyber-neonCyan' : 'text-cyber-neonPink'">{{ log.success ? '✓ 成功' : '✗ 失败' }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div class="mt-4 flex items-center justify-between text-xs">
            <div class="text-slate-500">显示 {{ filteredLogs.length }} 条，共 {{ totalLogCount }} 条记录</div>
            <div class="flex items-center gap-2">
              <button @click="currentPage--" :disabled="currentPage <= 1" class="rounded bg-white/5 px-3 py-1.5 disabled:opacity-30">上一页</button>
              <span class="text-slate-400">第 {{ currentPage }} 页 / {{ totalPages }}</span>
              <button @click="currentPage++" :disabled="currentPage >= totalPages" class="rounded bg-white/5 px-3 py-1.5 disabled:opacity-30">下一页</button>
            </div>
          </div>
        </GlassCard>
      </template>

      <template v-else-if="activeTab === 'system'">
        <div class="grid grid-cols-12 gap-4">
          <GlassCard title="部署与运行状态" class="col-span-12 2xl:col-span-6">
            <div class="grid gap-3 md:grid-cols-2">
              <div v-for="item in systemCards" :key="item.label" class="rounded-xl border border-white/10 bg-white/5 p-4">
                <div class="mb-1 text-xs text-slate-400">{{ item.label }}</div>
                <div class="text-lg font-semibold" :class="item.color">{{ item.value }}</div>
                <div class="mt-1 text-[11px] text-slate-500">{{ item.note }}</div>
              </div>
            </div>
          </GlassCard>

          <GlassCard title="系统配置摘要" class="col-span-12 2xl:col-span-6">
            <div class="space-y-3 text-xs">
              <div class="flex items-center justify-between rounded-lg bg-white/5 px-3 py-3">
                <span class="text-slate-400">数据刷新周期</span>
                <span class="text-slate-200">{{ refreshLabel }}</span>
              </div>
              <div class="flex items-center justify-between rounded-lg bg-white/5 px-3 py-3">
                <span class="text-slate-400">WebSocket状态</span>
                <span :class="systemSettings.websocket ? 'text-cyber-neonCyan' : 'text-slate-500'">{{ systemSettings.websocket ? '实时推送开启' : '关闭' }}</span>
              </div>
              <div class="flex items-center justify-between rounded-lg bg-white/5 px-3 py-3">
                <span class="text-slate-400">界面主题</span>
                <span class="text-slate-200">{{ systemSettings.darkMode ? '深色科技风' : '浅色模式' }}</span>
              </div>
              <div class="flex items-center justify-between rounded-lg bg-white/5 px-3 py-3">
                <span class="text-slate-400">页面布局</span>
                <span class="text-slate-200">{{ systemSettings.compact ? '紧凑模式' : '标准模式' }}</span>
              </div>
            </div>
          </GlassCard>
        </div>
      </template>

      <template v-else>
        <div class="grid grid-cols-12 gap-4">
          <GlassCard title="项目技术画像" class="col-span-12 2xl:col-span-7">
            <div class="grid gap-3 md:grid-cols-2">
              <div v-for="item in aboutCards" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
                <div class="mb-2 flex items-center gap-2 text-sm font-medium text-slate-100">
                  <span class="text-lg">{{ item.icon }}</span>
                  <span>{{ item.title }}</span>
                </div>
                <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
              </div>
            </div>
          </GlassCard>

          <GlassCard title="比赛表达建议" class="col-span-12 2xl:col-span-5">
            <div class="space-y-3">
              <div v-for="tip in defenseTips" :key="tip.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
                <div class="mb-2 text-sm font-medium text-slate-100">{{ tip.title }}</div>
                <div class="text-xs leading-6 text-slate-400">{{ tip.desc }}</div>
              </div>
            </div>
          </GlassCard>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import * as echarts from 'echarts'

import GlassCard from '../components/GlassCard.vue'
import { useAuthStore } from '../stores/auth.js'

const authStore = useAuthStore()

const activeTab = ref('overview')
const selectedGreenhouse = ref(1)
const compareGreenhouse1 = ref(1)
const compareGreenhouse2 = ref(2)
const activeTrendMetric = ref('temp')
const currentPage = ref(1)

const menuItems = [
  { key: 'overview', label: '成果总览', icon: '📊', hint: '指标、趋势与模拟成果' },
  { key: 'greenhouse', label: '参数口径', icon: '🧪', hint: '作物画像与目标边界' },
  { key: 'alerts', label: '预警机制', icon: '🚨', hint: '规则矩阵与通知逻辑' },
  { key: 'logs', label: '过程追溯', icon: '📋', hint: '动作记录与可复盘性' },
  { key: 'system', label: '部署状态', icon: '🖥️', hint: '运行摘要与系统配置' },
  { key: 'about', label: '答辩说明', icon: '🎓', hint: '技术画像与表达建议' }
]

const greenhouses = ref([
  { id: 1, name: '1号棚', crop: '藏红花', area: 500, score: 88 },
  { id: 2, name: '2号棚', crop: '人参', area: 400, score: 79 },
  { id: 3, name: '3号棚', crop: '名贵兰花', area: 300, score: 92 },
  { id: 4, name: '4号棚', crop: '铁皮石斛', area: 450, score: 74 }
])

const activeGreenhouse = computed(() => greenhouses.value.find((item) => item.id === selectedGreenhouse.value) || greenhouses.value[0])

const overviewStats = [
  { key: 'stability', label: '目标环境稳定性', value: '91.3%', trend: 'mock：近7日关键参数落入目标带比例', icon: '🛰️', color: 'text-cyber-neonCyan', badge: '核心指标', badgeClass: 'bg-cyber-neonCyan/15 text-cyber-neonCyan' },
  { key: 'efficiency', label: '异常处置时效', value: '< 3 min', trend: 'mock：从识别到动作下发平均耗时', icon: '⚡', color: 'text-cyber-neonPink', badge: '评委爱看', badgeClass: 'bg-cyber-neonPink/15 text-cyber-neonPink' },
  { key: 'inspection', label: '人工巡检替代率', value: '63%', trend: 'mock：减少重复巡棚与手工记录', icon: '🤖', color: 'text-cyber-neonViolet', badge: '效率提升', badgeClass: 'bg-cyber-neonViolet/15 text-cyber-neonViolet' },
  { key: 'sop', label: 'SOP闭环完成率', value: '95%', trend: 'mock：作业计划可追踪、可复盘', icon: '📚', color: 'text-slate-100', badge: '标准化', badgeClass: 'bg-white/10 text-slate-300' }
]

const mockAchievements = [
  { label: '曲线吻合度', value: '89.6%', trend: '↑ 5.8%', trendClass: 'text-cyber-neonCyan', valueClass: 'text-cyber-neonCyan', note: 'mock：数字孪生目标带拟合情况', progress: 90 },
  { label: '环境波动抑制', value: '36%', trend: '↓ 12%', trendClass: 'text-cyber-neonViolet', valueClass: 'text-cyber-neonViolet', note: 'mock：关键指标标准差下降幅度', progress: 82 },
  { label: '异常闭环率', value: '93%', trend: '↑ 9%', trendClass: 'text-cyber-neonPink', valueClass: 'text-cyber-neonPink', note: 'mock：预警后形成动作记录比例', progress: 93 }
]

const greenhouseRankings = [
  { id: 3, name: '3号棚-名贵兰花', score: 92, comment: '展示稳定性最佳，适合答辩主案例' },
  { id: 1, name: '1号棚-藏红花', score: 88, comment: '适合体现高附加值作物应用价值' },
  { id: 2, name: '2号棚-人参', score: 79, comment: '用于说明多品类迁移能力' },
  { id: 4, name: '4号棚-铁皮石斛', score: 74, comment: '适合解释预警与优化空间' }
]

const cropLegend = [
  { name: '藏红花', value: '25%', color: '#8B5CF6' },
  { name: '人参', value: '25%', color: '#22D3EE' },
  { name: '名贵兰花', value: '25%', color: '#EC4899' },
  { name: '铁皮石斛', value: '25%', color: '#F59E0B' }
]

const currentReadings = { temp: '22.3℃', humidity: '68%RH', soil: '35%', co2: '950ppm', ph: '6.2' }

const parameterTable = [
  { icon: '🌡️', name: '空气温度', range: '20–25℃', current: currentReadings.temp, currentClass: 'text-cyber-neonCyan', meaning: '影响代谢速率与蒸腾平衡，是高值作物基础控制参数。', action: '通风、加热、遮阳协同调节' },
  { icon: '💧', name: '空气湿度', range: '65–75%RH', current: currentReadings.humidity, currentClass: 'text-cyber-neonCyan', meaning: '影响气孔开闭与病害风险，需结合通风策略共同分析。', action: '雾化、排风、除湿联动' },
  { icon: '🌱', name: '土壤含水率', range: '30–45%', current: currentReadings.soil, currentClass: 'text-cyber-neonCyan', meaning: '反映根际供水状态，决定灌溉启动与时长策略。', action: '条件灌溉与排水调整' },
  { icon: '🌫️', name: 'CO₂浓度', range: '800–1200ppm', current: currentReadings.co2, currentClass: 'text-cyber-neonViolet', meaning: '与光合作用效率相关，可体现高值作物精细化调控能力。', action: '补碳与通风换气' },
  { icon: '⚗️', name: 'pH/营养液口径', range: '5.8–6.5', current: currentReadings.ph, currentClass: 'text-cyber-neonPink', meaning: '便于体现化学院学生在理化检测和离子平衡理解上的优势。', action: '营养液复核与配方修正' }
]

const irrigationSchedules = [
  { time: '08:00', duration: 5, frequency: '每日', enabled: true, conditions: '土壤湿度 < 30%' },
  { time: '14:00', duration: 3, frequency: '每日', enabled: true, conditions: '蒸腾高峰且土壤湿度 < 28%' },
  { time: '18:00', duration: 5, frequency: '每日', enabled: false, conditions: '夜间补水预案' }
]

const todayIrrigationMinutes = 8
const plannedIrrigationMinutes = 13

const stageTargets = [
  { stage: '缓苗期', days: '1–7天', temp: '21–23℃', humidity: '75–80%', co2: '700–900ppm', focus: '低应激稳态管理' },
  { stage: '营养生长期', days: '8–25天', temp: '22–25℃', humidity: '65–75%', co2: '800–1100ppm', focus: '促进叶面积与生物量积累' },
  { stage: '品质形成期', days: '26–45天', temp: '20–24℃', humidity: '60–70%', co2: '900–1200ppm', focus: '控制品质与活性成分表达' }
]

const alertRules = [
  { name: '温度异常', description: '温度超出目标带后触发预警', threshold: '±2℃', icon: '🌡️', enabled: true, duration: '1min', autoAction: true },
  { name: '湿度过低', description: '湿度偏低导致蒸腾失衡', threshold: '< 60%RH', icon: '💧', enabled: true, duration: '5min', autoAction: false },
  { name: '土壤干旱', description: '土壤含水率过低触发灌溉逻辑', threshold: '< 25%', icon: '🌵', enabled: true, duration: 'immediate', autoAction: true },
  { name: 'pH异常', description: '营养液酸碱度超界', threshold: '< 5.5 或 > 7.5', icon: '⚗️', enabled: false, duration: '5min', autoAction: false },
  { name: '设备离线', description: '传感器失联超过5分钟', threshold: '> 5min', icon: '📡', enabled: true, duration: 'immediate', autoAction: false },
  { name: 'CO₂浓度不足', description: '补碳不足影响光合效率', threshold: '< 600ppm', icon: '🌫️', enabled: true, duration: '15min', autoAction: false }
]

const durationMap = {
  immediate: '立即',
  '1min': '1分钟',
  '5min': '5分钟',
  '15min': '15分钟'
}

const alertStats = { critical: 2, warning: 5, info: 12 }
const alertTypes = [
  { name: '温度异常', count: 8, color: 'text-cyber-neonPink' },
  { name: '湿度偏低', count: 5, color: 'text-cyber-neonViolet' },
  { name: '设备离线', count: 3, color: 'text-cyber-neonCyan' },
  { name: '灌溉超时', count: 2, color: 'text-slate-400' }
]

const notificationSettings = { sms: true, email: false, app: true }

const operationLogs = ref([
  { id: 1, time: '2026-03-10 14:32:15', username: 'admin', userRole: 'admin', type: 'control', typeText: '设备控制', action: '手动启动灌溉 60 秒', greenhouse: '1号棚-藏红花', success: true },
  { id: 2, time: '2026-03-10 14:28:03', username: 'operator1', userRole: 'operator', type: 'config', typeText: '配置修改', action: '调整温度目标带至 20–25℃', greenhouse: '2号棚-人参', success: true },
  { id: 3, time: '2026-03-10 14:15:22', username: 'admin', userRole: 'admin', type: 'alert', typeText: '告警处理', action: '确认高温告警并记录处置意见', greenhouse: '1号棚-藏红花', success: true },
  { id: 4, time: '2026-03-10 13:45:10', username: 'viewer1', userRole: 'viewer', type: 'login', typeText: '登录注销', action: '用户登录系统查看实验态势', greenhouse: null, success: true },
  { id: 5, time: '2026-03-10 13:30:45', username: 'operator2', userRole: 'operator', type: 'control', typeText: '设备控制', action: '开启通风系统 80%', greenhouse: '3号棚-名贵兰花', success: true },
  { id: 6, time: '2026-03-10 13:15:18', username: 'admin', userRole: 'admin', type: 'config', typeText: '配置修改', action: '修订土壤湿度告警阈值', greenhouse: '全部大棚', success: true },
  { id: 7, time: '2026-03-10 12:58:33', username: 'operator1', userRole: 'operator', type: 'control', typeText: '设备控制', action: '手动启动灌溉 180 秒', greenhouse: '2号棚-人参', success: false },
  { id: 8, time: '2026-03-10 12:45:09', username: 'admin', userRole: 'admin', type: 'alert', typeText: '告警处理', action: '确认干旱告警并触发复盘', greenhouse: '4号棚-铁皮石斛', success: true }
])

const logFilter = reactive({ type: '', user: '', search: '' })
const pageSize = 6

const systemSettings = reactive({
  refreshInterval: 10000,
  websocket: true,
  darkMode: true,
  compact: false
})

const systemCards = [
  { label: '前端技术栈', value: 'Vue3 + Vite + ECharts', note: '适合快速构建比赛展示与实时看板', color: 'text-cyber-neonCyan' },
  { label: '后端技术栈', value: 'FastAPI + SQLite', note: '便于原型验证与接口快速扩展', color: 'text-cyber-neonViolet' },
  { label: '实时通信', value: 'WebSocket 已接入', note: '支持驾驶舱曲线与状态实时刷新', color: 'text-cyber-neonPink' },
  { label: '演示定位', value: '互联网+展示版', note: '强调价值表达、参数严谨与可复制推广', color: 'text-slate-100' }
]

const aboutCards = [
  { icon: '🌱', title: '项目定位', desc: '面向高附加值作物的数字孪生调控终端，强调从监测到控制再到复盘的闭环。' },
  { icon: '🧪', title: '专业特色', desc: '引入 pH、营养液、CO₂ 等理化参数口径，增强化学院学生参与项目时的专业可信度。' },
  { icon: '📈', title: '展示优势', desc: '兼具图表、表格、指标卡与场景化文案，更适合互联网+答辩现场。' },
  { icon: '🧩', title: '扩展方向', desc: '后续可继续补接算法预测、数据看板大屏、移动端巡检与成果对比实验。' }
]

const defenseTips = [
  { title: '先讲问题，再讲系统', desc: '用“高值作物对环境波动敏感，传统依赖经验”切入，再展示数字孪生闭环。' },
  { title: 'mock数据要说清口径', desc: '把模拟指标表述为“情景推演/阶段性预估值”，避免评委误解为真实生产结果。' },
  { title: '突出化学院优势', desc: '强调理化检测、营养液控制、参数边界与实验设计逻辑，这是你们的专业区分度。' }
]

const userRoleIcon = computed(() => {
  const role = authStore.user?.role
  return role === 'admin' ? '👑' : role === 'operator' ? '🔧' : '👁️'
})

const userRoleText = computed(() => {
  const role = authStore.user?.role
  return role === 'admin' ? '管理员' : role === 'operator' ? '操作员' : '观察员'
})

const userPermissions = computed(() => {
  const role = authStore.user?.role
  if (role === 'admin') return '全部权限'
  if (role === 'operator') return '控制 + 查看'
  return '仅查看'
})

const trendMetrics = [
  { key: 'temp', label: '温度' },
  { key: 'humidity', label: '湿度' },
  { key: 'soil', label: '土壤水分' },
  { key: 'co2', label: 'CO₂' }
]

const filteredLogSource = computed(() => {
  let logs = operationLogs.value
  if (logFilter.type) logs = logs.filter((item) => item.type === logFilter.type)
  if (logFilter.user) logs = logs.filter((item) => item.userRole === logFilter.user)
  if (logFilter.search) {
    const key = logFilter.search.toLowerCase()
    logs = logs.filter((item) =>
      item.action.toLowerCase().includes(key) ||
      item.username.toLowerCase().includes(key) ||
      (item.greenhouse && item.greenhouse.toLowerCase().includes(key))
    )
  }
  return logs
})

const totalLogCount = computed(() => filteredLogSource.value.length)
const totalPages = computed(() => Math.max(1, Math.ceil(totalLogCount.value / pageSize)))
const filteredLogs = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredLogSource.value.slice(start, start + pageSize)
})

const refreshLabel = computed(() => {
  if (systemSettings.refreshInterval === 5000) return '5秒'
  if (systemSettings.refreshInterval === 10000) return '10秒'
  if (systemSettings.refreshInterval === 30000) return '30秒'
  return '1分钟'
})

function getScoreColor(score) {
  if (score >= 85) return 'text-cyber-neonCyan'
  if (score >= 75) return 'text-cyber-neonViolet'
  return 'text-cyber-neonPink'
}

function getScoreBar(score) {
  if (score >= 85) return 'bg-cyber-neonCyan'
  if (score >= 75) return 'bg-cyber-neonViolet'
  return 'bg-cyber-neonPink'
}

function logTypeClass(type) {
  if (type === 'control') return 'bg-cyber-neonCyan/15 text-cyber-neonCyan'
  if (type === 'config') return 'bg-cyber-neonViolet/15 text-cyber-neonViolet'
  if (type === 'alert') return 'bg-cyber-neonPink/15 text-cyber-neonPink'
  return 'bg-white/10 text-slate-400'
}

function exportLogs() {
  window.dispatchEvent(new CustomEvent('app-toast', {
    detail: { type: 'success', msg: '已生成比赛展示用操作记录导出任务' }
  }))
}

const radarChartEl = ref(null)
const trendChartEl = ref(null)
const pieChartEl = ref(null)
let radarChart = null
let trendChart = null
let pieChart = null

function getRadarDataByGreenhouse(id) {
  const map = {
    1: [22, 70, 40, 78],
    2: [23, 66, 35, 82],
    3: [21, 72, 38, 88],
    4: [24, 63, 32, 74]
  }
  return map[id] || map[1]
}

function getTrendSeries(metric) {
  const source = {
    temp: { yName: '℃', a: [20.5, 21.2, 21.8, 22.4, 22.1, 21.7, 22.0], b: [19.8, 20.2, 20.9, 21.5, 21.1, 20.7, 20.9] },
    humidity: { yName: '%RH', a: [69, 71, 70, 68, 67, 69, 68], b: [64, 66, 65, 63, 62, 64, 65] },
    soil: { yName: '%', a: [33, 35, 37, 36, 35, 34, 35], b: [29, 31, 32, 33, 31, 30, 31] },
    co2: { yName: 'ppm', a: [860, 900, 930, 950, 920, 910, 940], b: [780, 820, 850, 870, 840, 830, 860] }
  }
  return source[metric] || source.temp
}

function initRadarChart() {
  if (!radarChartEl.value) return
  if (!radarChart) radarChart = echarts.init(radarChartEl.value, null, { renderer: 'canvas' })
  radarChart.setOption({
    backgroundColor: 'transparent',
    legend: {
      data: [
        greenhouses.value.find((g) => g.id === compareGreenhouse1.value)?.name || '棚1',
        greenhouses.value.find((g) => g.id === compareGreenhouse2.value)?.name || '棚2'
      ],
      textStyle: { color: '#94a3b8', fontSize: 10 },
      bottom: 0
    },
    radar: {
      indicator: [
        { name: '温度', max: 30 },
        { name: '湿度', max: 100 },
        { name: '土壤水分', max: 60 },
        { name: 'CO₂效率', max: 100 }
      ],
      axisName: { color: '#94a3b8', fontSize: 10 },
      splitArea: { areaStyle: { color: ['rgba(139,92,246,0.05)', 'rgba(139,92,246,0.02)'] } },
      axisLine: { lineStyle: { color: 'rgba(148,163,184,0.2)' } },
      splitLine: { lineStyle: { color: 'rgba(148,163,184,0.1)' } }
    },
    series: [{
      type: 'radar',
      data: [
        {
          value: getRadarDataByGreenhouse(compareGreenhouse1.value),
          name: greenhouses.value.find((g) => g.id === compareGreenhouse1.value)?.name || '棚1',
          areaStyle: { color: 'rgba(139,92,246,0.2)' },
          lineStyle: { color: '#8B5CF6' },
          itemStyle: { color: '#8B5CF6' }
        },
        {
          value: getRadarDataByGreenhouse(compareGreenhouse2.value),
          name: greenhouses.value.find((g) => g.id === compareGreenhouse2.value)?.name || '棚2',
          areaStyle: { color: 'rgba(34,211,238,0.18)' },
          lineStyle: { color: '#22D3EE' },
          itemStyle: { color: '#22D3EE' }
        }
      ]
    }]
  })
}

function initTrendChart() {
  if (!trendChartEl.value) return
  if (!trendChart) trendChart = echarts.init(trendChartEl.value, null, { renderer: 'canvas' })
  const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
  const series = getTrendSeries(activeTrendMetric.value)
  trendChart.setOption({
    backgroundColor: 'transparent',
    grid: { left: 45, right: 20, top: 30, bottom: 30 },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(10, 10, 30, 0.92)',
      borderColor: 'rgba(139, 92, 246, 0.3)',
      textStyle: { color: '#e2e8f0', fontSize: 10 }
    },
    legend: {
      data: ['1号棚', '2号棚'],
      textStyle: { color: '#94a3b8', fontSize: 10 },
      top: 0
    },
    xAxis: {
      type: 'category',
      data: days,
      axisLine: { lineStyle: { color: 'rgba(148,163,184,.35)' } },
      axisLabel: { color: 'rgba(226,232,240,.7)', fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      name: series.yName,
      nameTextStyle: { color: '#94a3b8', fontSize: 10 },
      axisLine: { show: false },
      splitLine: { lineStyle: { color: 'rgba(148,163,184,.12)' } },
      axisLabel: { color: 'rgba(226,232,240,.7)', fontSize: 10 }
    },
    series: [
      {
        name: '1号棚',
        type: 'line',
        smooth: true,
        data: series.a,
        lineStyle: { color: '#8B5CF6', width: 2 },
        itemStyle: { color: '#8B5CF6' },
        areaStyle: { color: 'rgba(139,92,246,0.08)' }
      },
      {
        name: '2号棚',
        type: 'line',
        smooth: true,
        data: series.b,
        lineStyle: { color: '#22D3EE', width: 2 },
        itemStyle: { color: '#22D3EE' },
        areaStyle: { color: 'rgba(34,211,238,0.06)' }
      }
    ]
  })
}

function initPieChart() {
  if (!pieChartEl.value) return
  if (!pieChart) pieChart = echarts.init(pieChartEl.value, null, { renderer: 'canvas' })
  pieChart.setOption({
    backgroundColor: 'transparent',
    series: [{
      type: 'pie',
      radius: ['42%', '72%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: false,
      itemStyle: {
        borderRadius: 6,
        borderColor: '#0a0a1a',
        borderWidth: 2
      },
      label: { show: false },
      labelLine: { show: false },
      data: cropLegend.map((item) => ({ value: 1, name: item.name, itemStyle: { color: item.color } }))
    }]
  })
}

function handleResize() {
  radarChart?.resize()
  trendChart?.resize()
  pieChart?.resize()
}

onMounted(() => {
  nextTick(() => {
    initRadarChart()
    initTrendChart()
    initPieChart()
  })
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  radarChart?.dispose()
  trendChart?.dispose()
  pieChart?.dispose()
})

watch([compareGreenhouse1, compareGreenhouse2], () => {
  initRadarChart()
})

watch(activeTrendMetric, () => {
  initTrendChart()
})

watch([() => logFilter.type, () => logFilter.user, () => logFilter.search], () => {
  currentPage.value = 1
})
</script>

<template>
  <div class="flex-1 flex flex-col bg-white overflow-hidden h-full">
    <!-- Header -->
    <header class="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between shadow-2xs z-20 shrink-0">
      <div class="flex items-center gap-3">
        <h2 class="text-base font-bold text-gray-900">WhatsApp Marketing</h2>
        <!-- 3 SubTabs -->
        <div class="flex items-center gap-1 bg-gray-100 p-0.5 rounded-lg text-xs font-semibold">
          <button
            @click="activeSubTab = 'templates'"
            :class="activeSubTab === 'templates' ? 'bg-white text-blue-600 shadow-2xs' : 'text-gray-500 hover:text-gray-800'"
            class="px-3 py-1 rounded-md transition flex items-center gap-1.5"
          >
            <span class="lucide-layout-template size-3.5" />
            Templates ({{ templates.length }})
          </button>
          <button
            @click="activeSubTab = 'composer'"
            :class="activeSubTab === 'composer' ? 'bg-white text-blue-600 shadow-2xs' : 'text-gray-500 hover:text-gray-800'"
            class="px-3 py-1 rounded-md transition flex items-center gap-1.5"
          >
            <span class="lucide-megaphone size-3.5" />
            Campaign Composer
          </button>
          <button
            @click="activeSubTab = 'history'"
            :class="activeSubTab === 'history' ? 'bg-white text-blue-600 shadow-2xs' : 'text-gray-500 hover:text-gray-800'"
            class="px-3 py-1 rounded-md transition flex items-center gap-1.5"
          >
            <span class="lucide-history size-3.5" />
            History
          </button>
        </div>
      </div>

      <div class="flex items-center gap-2">
        <Button
          v-if="activeSubTab === 'composer'"
          variant="solid"
          theme="green"
          size="sm"
          :loading="isLaunching"
          :disabled="isLaunching || !messageContent.trim() || selectedCustomerNames.length === 0"
          @click="sendCampaign"
        >
          <template #prefix>
            <span class="lucide-send size-3.5" />
          </template>
          Send Broadcast ({{ selectedCustomerNames.length }})
        </Button>

        <button
          v-if="activeSubTab === 'templates'"
          @click="openCreateTemplateModal"
          class="px-3 py-1.5 text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white rounded-lg flex items-center gap-1.5 transition shadow-2xs"
        >
          <span class="lucide-plus size-3.5" />
          Create Template
        </button>

        <button
          @click="refreshCurrentTab"
          class="px-3 py-1.5 text-xs font-semibold bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 rounded-lg flex items-center gap-1.5 transition"
        >
          <span :class="loadingCurrentTab ? 'animate-spin' : ''" class="lucide-refresh-cw size-3.5" />
          Refresh
        </button>
      </div>
    </header>

    <!-- SubTab 1: Templates Cards Grid View -->
    <div v-show="activeSubTab === 'templates'" class="flex-1 overflow-y-auto p-6 bg-gray-50/50">
      <div v-if="templates.length > 0" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-5">
        <div
          v-for="tmpl in templates"
          :key="tmpl.name"
          @click="openTemplateDetail(tmpl)"
          class="bg-white border border-gray-200 hover:border-blue-400 rounded-2xl overflow-hidden shadow-2xs hover:shadow-md transition-all cursor-pointer group flex flex-col"
        >
          <!-- Image Banner Preview -->
          <div class="h-36 bg-gray-100 border-b border-gray-100 relative overflow-hidden flex items-center justify-center">
            <img
              v-if="tmpl.image"
              :src="tmpl.image"
              alt="Template Banner"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
            <div v-else class="flex flex-col items-center justify-center text-gray-400 gap-1.5">
              <span class="lucide-image size-8 text-gray-300" />
              <span class="text-[10.5px]">No banner attached</span>
            </div>
          </div>

          <!-- Card Content -->
          <div class="p-4 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <div class="flex items-start justify-between gap-2">
                <h3 class="font-bold text-sm text-gray-900 group-hover:text-blue-600 transition truncate">
                  {{ tmpl.template_name || tmpl.name }}
                </h3>
                <span class="px-2 py-0.5 text-[10px] font-bold bg-emerald-50 text-emerald-700 rounded-full border border-emerald-100">
                  Active
                </span>
              </div>
              <p class="text-xs text-gray-600 mt-2 line-clamp-3 leading-relaxed break-words">
                {{ tmpl.message }}
              </p>
            </div>

            <!-- Card Bottom Bar -->
            <div class="pt-3 border-t border-gray-100 flex items-center justify-between">
              <span class="text-[10.5px] text-gray-400">{{ formatDate(tmpl.modified) }}</span>
              <div class="flex items-center gap-1.5" @click.stop>
                <button
                  @click="openTemplateDetail(tmpl)"
                  class="px-2.5 py-1 text-xs font-semibold text-gray-700 hover:text-blue-600 bg-gray-50 hover:bg-blue-50 rounded-lg transition"
                >
                  Edit
                </button>
                <button
                  @click="loadTemplateToComposer(tmpl)"
                  class="px-2.5 py-1 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition shadow-2xs flex items-center gap-1"
                >
                  <span class="lucide-send size-3" />
                  Use & Send
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty Templates -->
      <div v-else class="h-full flex flex-col items-center justify-center py-20 text-gray-400 text-center">
        <span class="lucide-layout-template size-12 text-gray-300 mb-3" />
        <h4 class="text-sm font-bold text-gray-700">No Templates Found</h4>
        <p class="text-xs text-gray-400 mt-1 max-w-sm">
          Create re-usable WhatsApp offer templates with banners and personalised customer tags.
        </p>
        <button
          @click="openCreateTemplateModal"
          class="mt-4 px-4 py-2 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-2xs transition"
        >
          + Create First Template
        </button>
      </div>
    </div>

    <!-- SubTab 2: Composer & Live Phone Preview -->
    <div v-show="activeSubTab === 'composer'" class="flex-1 overflow-hidden flex flex-col lg:flex-row">
      <!-- Left: Composer Form & Audience Selection -->
      <div class="flex-1 overflow-y-auto p-6 space-y-6">
        <!-- 1. Campaign Name & Template Selector -->
        <div class="bg-white border border-gray-200/90 rounded-2xl p-5 shadow-2xs space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold text-gray-700 uppercase tracking-wider flex items-center gap-2">
              <span class="size-2 rounded-full bg-blue-600" />
              1. Campaign & Template
            </h3>
            <button
              v-if="messageContent.trim()"
              @click="openSaveAsTemplateModal"
              class="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1 hover:underline"
            >
              <span class="lucide-bookmark size-3.5" />
              Save As Template
            </button>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Campaign Title</label>
              <input
                v-model="campaignName"
                type="text"
                placeholder="e.g. Diwali Festive Offer 2026"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-xs focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:outline-none bg-gray-50 hover:bg-white focus:bg-white transition"
              />
            </div>

            <div>
              <label class="block text-xs font-medium text-gray-600 mb-1">Load Saved Template</label>
              <select
                v-model="selectedTemplateName"
                @change="applyTemplate"
                class="w-full border border-gray-200 rounded-xl px-3 py-2 text-xs focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:outline-none bg-gray-50 hover:bg-white focus:bg-white transition"
              >
                <option value="">-- Choose Template (Optional) --</option>
                <option v-for="t in templates" :key="t.name" :value="t.name">
                  {{ t.template_name }}
                </option>
              </select>
            </div>
          </div>
        </div>

        <!-- 2. Message Content & Media -->
        <div class="bg-white border border-gray-200/90 rounded-2xl p-5 shadow-2xs space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold text-gray-700 uppercase tracking-wider flex items-center gap-2">
              <span class="size-2 rounded-full bg-blue-600" />
              2. Message Content
            </h3>
            <!-- Placeholder Tags -->
            <div class="flex items-center gap-1.5">
              <span class="text-[11px] text-gray-400">Insert tag:</span>
              <button
                @click="insertTag('{customer_name}')"
                class="px-2 py-0.5 text-[11px] font-mono bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-md transition font-semibold"
              >
                {customer_name}
              </button>
              <button
                @click="insertTag('{mobile_no}')"
                class="px-2 py-0.5 text-[11px] font-mono bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-md transition font-semibold"
              >
                {mobile_no}
              </button>
            </div>
          </div>

          <div>
            <textarea
              v-model="messageContent"
              rows="5"
              placeholder="Write your promotional offer message here... E.g. Dear {customer_name}, enjoy exclusive 20% off on your next visit this week!"
              class="w-full border border-gray-200 rounded-xl p-3 text-xs leading-relaxed focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:outline-none bg-gray-50 hover:bg-white focus:bg-white transition resize-none"
            />
          </div>

          <!-- Image Upload / Attach Image -->
          <div>
            <label class="block text-xs font-medium text-gray-600 mb-1">Attach Offer Banner / Photo (Optional)</label>
            <div class="flex items-center gap-3">
              <input
                ref="fileInputRef"
                type="file"
                accept="image/*"
                @change="handleImageUpload"
                class="hidden"
              />
              <button
                @click="$refs.fileInputRef.click()"
                type="button"
                :disabled="uploadingImage"
                class="px-3.5 py-2 text-xs font-semibold bg-gray-50 hover:bg-gray-100 text-gray-700 border border-gray-200 rounded-xl flex items-center gap-2 transition"
              >
                <span v-if="uploadingImage" class="lucide-loader-2 size-3.5 animate-spin text-blue-600" />
                <span v-else class="lucide-image size-3.5 text-gray-500" />
                <span>{{ imageUrl ? 'Change Image' : 'Upload Banner / Image' }}</span>
              </button>

              <div v-if="imageUrl" class="flex items-center gap-2 bg-blue-50/80 border border-blue-100 px-3 py-1.5 rounded-xl">
                <span class="text-xs text-blue-800 font-medium truncate max-w-xs">{{ imageUrl.split('/').pop() }}</span>
                <button @click="imageUrl = ''" class="text-blue-500 hover:text-blue-800 text-xs font-bold">✕</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Target Audience (Customers) -->
        <div class="bg-white border border-gray-200/90 rounded-2xl p-5 shadow-2xs space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-xs font-bold text-gray-700 uppercase tracking-wider flex items-center gap-2">
              <span class="size-2 rounded-full bg-blue-600" />
              3. Target Audience ({{ selectedCustomerNames.length }} / {{ validCustomers.length }} Selected)
            </h3>

            <div class="flex items-center gap-2">
              <button
                @click="selectAllCustomers"
                class="text-xs text-blue-600 hover:text-blue-800 font-semibold transition"
              >
                Select All
              </button>
              <span class="text-gray-300">|</span>
              <button
                @click="clearCustomerSelection"
                class="text-xs text-gray-500 hover:text-gray-700 transition"
              >
                Deselect
              </button>
            </div>
          </div>

          <!-- Quick Customer Search -->
          <div class="relative">
            <span class="lucide-search absolute left-3 top-2.5 size-3.5 text-gray-400" />
            <input
              v-model="customerFilterQuery"
              type="text"
              placeholder="Filter recipient list by name or phone..."
              class="w-full pl-8 pr-3 py-1.5 text-xs bg-gray-50 border border-gray-200 rounded-xl focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
          </div>

          <!-- Customer Badges / Selectable Table -->
          <div class="max-h-56 overflow-y-auto border border-gray-100 rounded-xl divide-y divide-gray-100">
            <div
              v-for="c in filteredRecipients"
              :key="c.name"
              @click="toggleCustomerSelection(c.name)"
              class="px-3.5 py-2 flex items-center justify-between hover:bg-blue-50/50 cursor-pointer text-xs transition"
            >
              <div class="flex items-center gap-2.5">
                <input
                  type="checkbox"
                  :checked="selectedCustomerNames.includes(c.name)"
                  @click.stop="toggleCustomerSelection(c.name)"
                  class="rounded text-blue-600 focus:ring-blue-500 size-3.5"
                />
                <span class="font-bold text-gray-800">{{ c.customer_name || c.name }}</span>
                <span class="text-[11px] font-mono text-gray-500">{{ c.mobile_no }}</span>
              </div>
              <span class="text-[11px] text-gray-400">Spent: ₹{{ Number(c.total_spent || 0).toFixed(0) }}</span>
            </div>

            <div v-if="filteredRecipients.length === 0" class="py-6 text-center text-xs text-gray-400">
              No matching customers with mobile numbers found.
            </div>
          </div>
        </div>

        <!-- Launch Broadcast Sticky Bar -->
        <div class="sticky bottom-0 bg-white/95 backdrop-blur-xs border-t border-gray-200 py-3 -mx-6 px-6 shadow-md flex items-center justify-between z-10">
          <div class="text-xs text-gray-500 flex items-center gap-2">
            <span class="lucide-zap size-4 text-amber-500" />
            <span>Superfast Delivery: 1–2 sec delay</span>
          </div>

          <Button
            variant="solid"
            theme="green"
            size="md"
            :loading="isLaunching"
            :disabled="isLaunching || !messageContent.trim() || selectedCustomerNames.length === 0"
            @click="sendCampaign"
          >
            <template #prefix>
              <span class="lucide-send size-4" />
            </template>
            Launch Broadcast to {{ selectedCustomerNames.length }} Customers
          </Button>
        </div>
      </div>

      <!-- Right: Real-time WhatsApp Phone Mockup Preview -->
      <div class="w-full lg:w-96 bg-gray-100 border-t lg:border-t-0 lg:border-l border-gray-200 p-6 flex flex-col items-center justify-center shrink-0">
        <div class="text-xs font-bold text-gray-500 uppercase tracking-wider mb-3">Customer Phone Preview</div>

        <!-- Phone Shell -->
        <div class="w-72 bg-neutral-900 rounded-[38px] p-3 shadow-2xl border-4 border-neutral-800 flex flex-col">
          <!-- Notch / Camera -->
          <div class="w-20 h-4 bg-neutral-800 rounded-full mx-auto mb-2 shrink-0" />

          <!-- Screen Container -->
          <div class="bg-[#efeae2] rounded-[26px] overflow-hidden flex flex-col h-[460px] shadow-inner text-xs">
            <!-- WhatsApp Top Bar -->
            <div class="bg-[#008069] text-white px-3 py-2 flex items-center gap-2 shrink-0 shadow-xs">
              <div class="size-6 rounded-full bg-white/20 flex items-center justify-center text-[10px] font-bold">
                T
              </div>
              <div class="flex-1 truncate">
                <div class="font-bold text-[11px] leading-tight">Tailor Store</div>
                <div class="text-[9px] text-white/80 leading-tight">online</div>
              </div>
            </div>

            <!-- Chat Wallpaper / Bubble Area (Scrollable) -->
            <div class="flex-1 min-h-0 p-3 overflow-y-auto overscroll-contain flex flex-col justify-start space-y-2">
              <!-- Message Bubble -->
              <div class="bg-white rounded-lg rounded-tl-none p-2.5 shadow-xs w-full max-w-[92%] border border-gray-200/50 space-y-2 self-start animate-in fade-in shrink-0">
                <!-- Attached Image Preview -->
                <div v-if="imageUrl" class="rounded-md overflow-hidden bg-gray-100 max-h-48 shrink-0">
                  <img :src="imageUrl" alt="Offer preview" class="w-full h-full object-cover" />
                </div>

                <!-- Text -->
                <p class="text-[11.5px] text-gray-800 whitespace-pre-wrap leading-relaxed break-words">
                  {{ previewMessageText || 'Your offer message will appear here...' }}
                </p>

                <div class="flex justify-end items-center gap-1 text-[9px] text-gray-400">
                  <span>10:30 AM</span>
                  <span class="text-blue-500 font-bold">✓✓</span>
                </div>
              </div>
            </div>

            <!-- Mock Bottom Input Bar -->
            <div class="bg-[#f0f2f5] px-3 py-2 flex items-center gap-2 border-t border-gray-200 shrink-0">
              <div class="bg-white rounded-full px-3 py-1 flex-1 text-[11px] text-gray-400">
                Message...
              </div>
              <div class="size-7 rounded-full bg-[#008069] text-white flex items-center justify-center text-xs">
                ➤
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- SubTab 3: Campaign History & Real-Time Delivery Logs -->
    <div v-show="activeSubTab === 'history'" class="flex-1 overflow-auto p-6">
      <table class="w-full text-left text-xs border-collapse">
        <thead class="bg-gray-50 border-b border-gray-200 text-gray-500 font-semibold uppercase text-[11px]">
          <tr>
            <th class="py-3 px-6">Campaign ID / Name</th>
            <th class="py-3 px-6">Date</th>
            <th class="py-3 px-6">Status</th>
            <th class="py-3 px-6 text-center">Recipients</th>
            <th class="py-3 px-6 text-center">Delivered</th>
            <th class="py-3 px-6 text-center">Failed</th>
            <th class="py-3 px-6 text-center">Action</th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-100 font-medium text-gray-700">
          <tr
            v-for="cmp in campaigns"
            :key="cmp.name"
            class="hover:bg-blue-50/40 transition cursor-pointer"
            @click="openCampaignLog(cmp.name)"
          >
            <td class="py-3.5 px-6">
              <div class="font-bold text-gray-900">{{ cmp.campaign_name }}</div>
              <div class="text-[10.5px] font-mono text-gray-400">{{ cmp.name }}</div>
            </td>
            <td class="py-3.5 px-6 text-gray-600">{{ formatDate(cmp.creation) }}</td>
            <td class="py-3.5 px-6">
              <span
                class="px-2.5 py-0.5 rounded-full text-[10.5px] font-bold"
                :class="statusBadgeClass(cmp.status)"
              >
                {{ cmp.status }}
              </span>
            </td>
            <td class="py-3.5 px-6 text-center font-bold text-gray-800">{{ cmp.total_recipients }}</td>
            <td class="py-3.5 px-6 text-center font-bold text-emerald-600">{{ cmp.sent_count }}</td>
            <td class="py-3.5 px-6 text-center font-bold text-red-600">{{ cmp.failed_count }}</td>
            <td class="py-3.5 px-6 text-center" @click.stop>
              <button
                @click="openCampaignLog(cmp.name)"
                class="px-2.5 py-1 text-xs font-semibold text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg transition"
              >
                View Delivery Logs
              </button>
            </td>
          </tr>

          <tr v-if="campaigns.length === 0">
            <td colspan="7" class="py-16 text-center text-gray-400">
              No campaigns launched yet. Create your first broadcast from the Composer tab!
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Template Detail & Edit Modal with Frappe UI Controls -->
    <div
      v-if="selectedTemplateModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs"
      @click.self="selectedTemplateModal = null"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-gray-100 w-full max-w-lg overflow-hidden flex flex-col">
        <!-- Modal Header -->
        <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-gray-50/80">
          <div class="flex items-center gap-2">
            <span class="lucide-layout-template size-4 text-blue-600" />
            <h3 class="text-sm font-bold text-gray-900">
              {{ isCreatingNewTemplate ? 'Create New Template' : 'Edit Template' }}
            </h3>
          </div>
          <button @click="selectedTemplateModal = null" class="text-gray-400 hover:text-gray-600 text-base leading-none">✕</button>
        </div>

        <!-- Form Body -->
        <div class="p-6 space-y-4 overflow-y-auto max-h-[75vh]">
          <FormControl
            label="Template Title"
            type="text"
            size="sm"
            v-model="templateFormTitle"
            placeholder="e.g. Festival Offer 2026"
            required
          />

          <!-- Image Preview & Upload -->
          <div>
            <label class="block text-xs font-semibold text-gray-700 mb-1.5">Attached Banner / Image</label>
            <div class="flex items-center gap-3">
              <input
                ref="templateImageInputRef"
                type="file"
                accept="image/*"
                @change="handleTemplateImageUpload"
                class="hidden"
              />
              <Button
                variant="subtle"
                size="sm"
                :loading="uploadingTemplateImage"
                @click="$refs.templateImageInputRef.click()"
              >
                <template #prefix>
                  <span class="lucide-image size-3.5" />
                </template>
                {{ templateFormImage ? 'Change Image' : 'Upload Image' }}
              </Button>

              <div v-if="templateFormImage" class="flex items-center gap-2 bg-blue-50 px-2.5 py-1 rounded-lg border border-blue-100">
                <span class="text-xs text-blue-700 font-medium truncate max-w-xs">{{ templateFormImage.split('/').pop() }}</span>
                <button @click="templateFormImage = ''" class="text-blue-500 hover:text-blue-800 text-xs font-bold">✕</button>
              </div>
            </div>

            <!-- Image thumbnail if available -->
            <div v-if="templateFormImage" class="mt-2.5 rounded-xl overflow-hidden border border-gray-200 h-28 bg-gray-100">
              <img :src="templateFormImage" alt="Template banner" class="w-full h-full object-cover" />
            </div>
          </div>

          <!-- Message Textarea -->
          <div>
            <div class="flex items-center justify-between mb-1.5">
              <label class="block text-xs font-semibold text-gray-700">Message Content</label>
              <div class="flex items-center gap-1">
                <span class="text-[10px] text-gray-400">Insert tag:</span>
                <button
                  type="button"
                  @click="insertTemplateTag('{customer_name}')"
                  class="px-1.5 py-0.5 text-[10px] font-mono bg-blue-50 text-blue-700 rounded hover:bg-blue-100"
                >
                  {customer_name}
                </button>
                <button
                  type="button"
                  @click="insertTemplateTag('{mobile_no}')"
                  class="px-1.5 py-0.5 text-[10px] font-mono bg-blue-50 text-blue-700 rounded hover:bg-blue-100"
                >
                  {mobile_no}
                </button>
              </div>
            </div>

            <textarea
              v-model="templateFormMessage"
              rows="4"
              placeholder="Enter message with {customer_name} placeholders..."
              class="w-full border border-gray-300 rounded-xl p-3 text-xs focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 focus:outline-none resize-none"
            />
          </div>
        </div>

        <!-- Modal Footer with Save & Use Button -->
        <div class="px-6 py-3.5 border-t border-gray-200 bg-gray-50 flex items-center justify-between shrink-0">
          <Button
            v-if="!isCreatingNewTemplate"
            variant="outline"
            theme="blue"
            size="sm"
            @click="useTemplateFromModal"
          >
            <template #prefix>
              <span class="lucide-send size-3.5" />
            </template>
            Use in Composer
          </Button>
          <div v-else />

          <div class="flex items-center gap-2">
            <Button
              variant="subtle"
              size="sm"
              @click="selectedTemplateModal = null"
            >
              Cancel
            </Button>
            <Button
              variant="solid"
              theme="blue"
              size="sm"
              :loading="isSavingTemplate"
              :disabled="isSavingTemplate || !templateFormTitle.trim() || !templateFormMessage.trim()"
              @click="saveTemplateFromModal"
            >
              {{ isCreatingNewTemplate ? 'Create Template' : 'Save Changes' }}
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Campaign Log Detail Modal -->
    <div
      v-if="selectedCampaignLog"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs"
      @click.self="selectedCampaignLog = null"
    >
      <div class="bg-white rounded-2xl shadow-2xl border border-gray-100 w-full max-w-4xl max-h-[88vh] flex flex-col overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200 flex items-center justify-between bg-gray-50/80">
          <div>
            <h3 class="font-bold text-gray-900 text-sm">{{ selectedCampaignLog.campaign_name }}</h3>
            <p class="text-xs text-gray-400 font-mono mt-0.5">{{ selectedCampaignLog.name }}</p>
          </div>
          <button @click="selectedCampaignLog = null" class="text-gray-400 hover:text-gray-600 text-lg">✕</button>
        </div>

        <div class="grid grid-cols-3 gap-3 p-4 bg-gray-50 border-b border-gray-200 shrink-0">
          <div class="bg-white p-3 rounded-xl border border-gray-200 shadow-2xs">
            <span class="text-[10px] text-gray-400 uppercase font-semibold">Total</span>
            <div class="text-base font-bold text-gray-800">{{ selectedCampaignLog.total_recipients }}</div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-gray-200 shadow-2xs">
            <span class="text-[10px] text-gray-400 uppercase font-semibold">Sent</span>
            <div class="text-base font-bold text-emerald-600">{{ selectedCampaignLog.sent_count }}</div>
          </div>
          <div class="bg-white p-3 rounded-xl border border-gray-200 shadow-2xs">
            <span class="text-[10px] text-gray-400 uppercase font-semibold">Failed</span>
            <div class="text-base font-bold text-red-600">{{ selectedCampaignLog.failed_count }}</div>
          </div>
        </div>

        <!-- Recipients Table -->
        <div class="flex-1 overflow-auto p-4">
          <table class="w-full text-left text-xs border-collapse">
            <thead class="bg-gray-100 text-gray-600 uppercase text-[10.5px]">
              <tr>
                <th class="py-2.5 px-3">Customer</th>
                <th class="py-2.5 px-3">Mobile</th>
                <th class="py-2.5 px-3">Status</th>
                <th class="py-2.5 px-3">Delivery Time / Info</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-100">
              <tr v-for="(r, idx) in selectedCampaignLog.recipients" :key="idx" class="hover:bg-gray-50">
                <td class="py-2.5 px-3 font-semibold text-gray-900">{{ r.customer_name || r.customer }}</td>
                <td class="py-2.5 px-3 font-mono text-gray-600">{{ r.mobile_no }}</td>
                <td class="py-2.5 px-3">
                  <span
                    class="px-2 py-0.5 rounded-full text-[10px] font-bold"
                    :class="r.status === 'Sent' ? 'bg-emerald-100 text-emerald-700' : (r.status === 'Failed' ? 'bg-red-100 text-red-700' : 'bg-amber-100 text-amber-700')"
                  >
                    {{ r.status }}
                  </span>
                </td>
                <td class="py-2.5 px-3 text-gray-500">
                  <span v-if="r.sent_at">{{ formatDate(r.sent_at) }}</span>
                  <span v-else-if="r.error_message" class="text-red-500">{{ r.error_message }}</span>
                  <span v-else class="text-gray-400 italic">In Queue</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="px-6 py-3 border-t border-gray-200 bg-gray-50 flex justify-end">
          <Button variant="subtle" size="sm" @click="selectedCampaignLog = null">
            Close
          </Button>
        </div>
      </div>
    </div>

    <!-- Confirm Broadcast Dialog (Frappe UI) -->
    <Dialog
      v-model="showConfirmBroadcast"
      :options="{
        title: 'Launch WhatsApp Campaign',
        size: 'sm',
      }"
    >
      <template #body-content>
        <div class="space-y-3 py-2 text-xs text-gray-600">
          <p>
            Are you sure you want to send this broadcast to
            <strong class="text-gray-900 font-bold">{{ selectedCustomerNames.length }} customers</strong>?
          </p>
          <div class="bg-blue-50 border border-blue-200 rounded-xl p-3 text-blue-800 text-[11px] flex items-start gap-2">
            <span class="lucide-zap size-4 text-amber-500 shrink-0 mt-0.5" />
            <span>Superfast delivery enabled: messages will be sent instantly with 1–2 sec intervals.</span>
          </div>
        </div>
      </template>

      <template #actions>
        <div class="flex items-center justify-end gap-2 pt-2">
          <Button variant="subtle" size="sm" @click="showConfirmBroadcast = false">
            Cancel
          </Button>
          <Button
            variant="solid"
            theme="green"
            size="sm"
            :loading="isLaunching"
            @click="executeSendCampaign"
          >
            Yes, Send Broadcast
          </Button>
        </div>
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import { FormControl, Button, Dialog } from 'frappe-ui';

const activeSubTab = ref('templates');

const campaignName = ref('');
const selectedTemplateName = ref('');
const messageContent = ref('');
const imageUrl = ref('');
const uploadingImage = ref(false);

const templates = ref([]);
const customers = ref([]);
const selectedCustomerNames = ref([]);
const customerFilterQuery = ref('');

const isLaunching = ref(false);
const showConfirmBroadcast = ref(false);

// Template Modal State
const selectedTemplateModal = ref(null);
const isCreatingNewTemplate = ref(false);
const templateFormTitle = ref('');
const templateFormMessage = ref('');
const templateFormImage = ref('');
const uploadingTemplateImage = ref(false);
const isSavingTemplate = ref(false);

const campaigns = ref([]);
const loadingCampaigns = ref(false);
const selectedCampaignLog = ref(null);

const loadingCurrentTab = computed(() => loadingCampaigns.value || uploadingImage.value || isSavingTemplate.value);

const validCustomers = computed(() => {
  return customers.value.filter((c) => c.mobile_no && c.mobile_no.trim().length >= 10);
});

const filteredRecipients = computed(() => {
  if (!customerFilterQuery.value.trim()) return validCustomers.value;
  const q = customerFilterQuery.value.toLowerCase().trim();
  return validCustomers.value.filter((c) =>
    (c.customer_name || c.name || '').toLowerCase().includes(q) ||
    (c.mobile_no || '').includes(q)
  );
});

const previewMessageText = computed(() => {
  if (!messageContent.value) return '';
  const sampleName = validCustomers.value[0]?.customer_name || 'Customer';
  const samplePhone = validCustomers.value[0]?.mobile_no || '9876543210';
  return messageContent.value
    .replace(/{customer_name}/g, sampleName)
    .replace(/{mobile_no}/g, samplePhone);
});

function insertTag(tag) {
  messageContent.value = (messageContent.value || '') + ` ${tag} `;
}

function insertTemplateTag(tag) {
  templateFormMessage.value = (templateFormMessage.value || '') + ` ${tag} `;
}

function selectAllCustomers() {
  selectedCustomerNames.value = validCustomers.value.map((c) => c.name);
}

function clearCustomerSelection() {
  selectedCustomerNames.value = [];
}

function toggleCustomerSelection(name) {
  const idx = selectedCustomerNames.value.indexOf(name);
  if (idx > -1) {
    selectedCustomerNames.value.splice(idx, 1);
  } else {
    selectedCustomerNames.value.push(name);
  }
}

function openCreateTemplateModal() {
  isCreatingNewTemplate.value = true;
  templateFormTitle.value = '';
  templateFormMessage.value = '';
  templateFormImage.value = '';
  selectedTemplateModal.value = true;
}

function openTemplateDetail(tmpl) {
  isCreatingNewTemplate.value = false;
  templateFormTitle.value = tmpl.template_name || tmpl.name;
  templateFormMessage.value = tmpl.message;
  templateFormImage.value = tmpl.image || '';
  selectedTemplateModal.value = tmpl;
}

function openSaveAsTemplateModal() {
  isCreatingNewTemplate.value = true;
  templateFormTitle.value = campaignName.value || '';
  templateFormMessage.value = messageContent.value || '';
  templateFormImage.value = imageUrl.value || '';
  selectedTemplateModal.value = true;
}

function loadTemplateToComposer(tmpl) {
  selectedTemplateName.value = tmpl.name;
  messageContent.value = tmpl.message;
  imageUrl.value = tmpl.image || '';
  campaignName.value = `${tmpl.template_name} Campaign`;
  activeSubTab.value = 'composer';
}

function useTemplateFromModal() {
  if (selectedTemplateModal.value) {
    messageContent.value = templateFormMessage.value;
    imageUrl.value = templateFormImage.value || '';
    campaignName.value = `${templateFormTitle.value} Campaign`;
    selectedTemplateModal.value = null;
    activeSubTab.value = 'composer';
  }
}

function applyTemplate() {
  const t = templates.value.find((item) => item.name === selectedTemplateName.value);
  if (t) {
    messageContent.value = t.message;
    imageUrl.value = t.image || '';
    if (!campaignName.value) {
      campaignName.value = `${t.template_name} Campaign`;
    }
  }
}

async function handleTemplateImageUpload(e) {
  const file = e.target.files?.[0];
  if (!file) return;

  uploadingTemplateImage.value = true;
  const formData = new FormData();
  formData.append('file', file);
  formData.append('is_private', '0');

  try {
    const res = await fetch('/api/method/upload_file', {
      method: 'POST',
      headers: { 'X-Frappe-CSRF-Token': window.csrf_token || '' },
      body: formData,
    });
    const json = await res.json();
    if (json.message?.file_url) {
      templateFormImage.value = json.message.file_url;
    }
  } catch (err) {
    alert('Failed to upload image: ' + err.message);
  } finally {
    uploadingTemplateImage.value = false;
  }
}

async function saveTemplateFromModal() {
  if (!templateFormTitle.value.trim() || !templateFormMessage.value.trim()) return;

  isSavingTemplate.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.save_whatsapp_template', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({
        template_name: templateFormTitle.value.trim(),
        message: templateFormMessage.value,
        image: templateFormImage.value,
      }),
    });
    const json = await res.json();
    if (json.message) {
      selectedTemplateModal.value = null;
      await fetchTemplates();
    }
  } catch (err) {
    alert('Failed to save template: ' + err.message);
  } finally {
    isSavingTemplate.value = false;
  }
}

async function handleImageUpload(e) {
  const file = e.target.files?.[0];
  if (!file) return;

  uploadingImage.value = true;
  const formData = new FormData();
  formData.append('file', file);
  formData.append('is_private', '0');

  try {
    const res = await fetch('/api/method/upload_file', {
      method: 'POST',
      headers: { 'X-Frappe-CSRF-Token': window.csrf_token || '' },
      body: formData,
    });
    const json = await res.json();
    if (json.message?.file_url) {
      imageUrl.value = json.message.file_url;
    }
  } catch (err) {
    alert('Failed to upload image: ' + err.message);
  } finally {
    uploadingImage.value = false;
  }
}

function sendCampaign() {
  if (!messageContent.value.trim() || selectedCustomerNames.value.length === 0) return;
  showConfirmBroadcast.value = true;
}

async function executeSendCampaign() {
  showConfirmBroadcast.value = false;
  isLaunching.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.start_whatsapp_campaign', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({
        campaign_name: campaignName.value.trim() || `Campaign ${new Date().toLocaleDateString('en-IN')}`,
        message: messageContent.value,
        image: imageUrl.value,
        template: selectedTemplateName.value,
        customer_names: selectedCustomerNames.value,
      }),
    });
    const json = await res.json();
    if (json.message?.campaign) {
      activeSubTab.value = 'history';
      fetchCampaigns();
    }
  } catch (err) {
    console.error('Failed to start campaign:', err);
  } finally {
    isLaunching.value = false;
  }
}

async function fetchTemplates() {
  try {
    const res = await fetch('/api/method/tailorms.api.get_whatsapp_templates', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
    });
    const json = await res.json();
    templates.value = json.message || [];
  } catch (err) {
    console.error('Failed to load templates', err);
  }
}

async function fetchCustomers() {
  try {
    const res = await fetch('/api/method/tailorms.api.get_customer_list', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
    });
    const json = await res.json();
    customers.value = json.message || [];
    selectedCustomerNames.value = validCustomers.value.map((c) => c.name);
  } catch (err) {
    console.error('Failed to load customers', err);
  }
}

async function fetchCampaigns() {
  loadingCampaigns.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_whatsapp_campaigns', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
    });
    const json = await res.json();
    campaigns.value = json.message || [];
  } catch (err) {
    console.error('Failed to load campaigns', err);
  } finally {
    loadingCampaigns.value = false;
  }
}

function refreshCurrentTab() {
  fetchTemplates();
  fetchCustomers();
  fetchCampaigns();
}

async function openCampaignLog(cmpName) {
  try {
    const res = await fetch('/api/method/tailorms.api.get_campaign_detail', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Frappe-CSRF-Token': window.csrf_token || '' },
      body: JSON.stringify({ campaign_name: cmpName }),
    });
    const json = await res.json();
    if (json.message) {
      selectedCampaignLog.value = json.message;
    }
  } catch (err) {
    alert('Failed to load campaign logs: ' + err.message);
  }
}

function formatDate(d) {
  if (!d) return '—';
  try {
    return new Date(d).toLocaleString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  } catch {
    return d;
  }
}

function statusBadgeClass(st) {
  switch (st) {
    case 'Completed': return 'bg-emerald-100 text-emerald-800';
    case 'In Progress': return 'bg-blue-100 text-blue-800';
    case 'Queued': return 'bg-amber-100 text-amber-800';
    case 'Failed': return 'bg-red-100 text-red-800';
    default: return 'bg-gray-100 text-gray-800';
  }
}

function handleEscKey(e) {
  if (e.key === 'Escape') {
    if (selectedTemplateModal.value) selectedTemplateModal.value = null;
    else if (selectedCampaignLog.value) selectedCampaignLog.value = null;
  }
}

onMounted(() => {
  fetchTemplates();
  fetchCustomers();
  fetchCampaigns();
  document.addEventListener('keydown', handleEscKey);
});

onBeforeUnmount(() => {
  document.removeEventListener('keydown', handleEscKey);
});
</script>

<template>
  <div class="h-screen w-screen flex bg-gray-50 overflow-hidden font-sans select-none">
    <!-- Left Compact Icon-Style Sidebar (Light Theme, Collapsed with Visible Labels) -->
    <aside class="w-16 bg-white border-r border-gray-200 flex flex-col justify-between items-center py-3 flex-shrink-0 z-30 shadow-xs">
      <div class="flex flex-col items-center gap-4 w-full">
        <!-- Brand Icon -->
        <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center shadow-xs text-white font-bold text-lg">
          <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
            <path d="M20 7h-4V4c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v3H4c-1.1 0-2 .9-2 2v11c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V9c0-1.1-.9-2-2-2zM10 4h4v3h-4V4zm10 16H4V9h16v11z"/>
          </svg>
        </div>

        <!-- Navigation Links (Vertical Icon + Label Badge) -->
        <nav class="flex flex-col items-center gap-2 w-full px-1">
          <!-- 1. POS -->
          <button
            @click="currentTab = 'pos'"
            :class="currentTab === 'pos' ? 'bg-blue-50 text-blue-600 border border-blue-200 font-bold shadow-2xs' : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900 font-medium'"
            class="w-full flex flex-col items-center justify-center py-2 rounded-xl transition group"
            title="Point of Sale"
          >
            <span class="text-lg">🛒</span>
            <span class="text-[10px] mt-0.5 leading-tight tracking-tight">POS</span>
          </button>

          <!-- 2. Invoices -->
          <button
            @click="switchTab('invoices')"
            :class="currentTab === 'invoices' ? 'bg-blue-50 text-blue-600 border border-blue-200 font-bold shadow-2xs' : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900 font-medium'"
            class="w-full flex flex-col items-center justify-center py-2 rounded-xl transition group"
            title="Sales Invoices"
          >
            <span class="text-lg">🧾</span>
            <span class="text-[10px] mt-0.5 leading-tight tracking-tight">Invoices</span>
          </button>

          <!-- 3. Stock Entry -->
          <button
            @click="switchTab('stock')"
            :class="currentTab === 'stock' ? 'bg-blue-50 text-blue-600 border border-blue-200 font-bold shadow-2xs' : 'text-gray-500 hover:bg-gray-100 hover:text-gray-900 font-medium'"
            class="w-full flex flex-col items-center justify-center py-2 rounded-xl transition group"
            title="Stock Entries"
          >
            <span class="text-lg">📦</span>
            <span class="text-[9.5px] mt-0.5 leading-tight tracking-tight">Stock</span>
          </button>
        </nav>
      </div>

      <!-- Bottom Desk Link -->
      <div class="w-full px-1 flex flex-col items-center">
        <button
          @click="goToDesk"
          class="w-full flex flex-col items-center justify-center py-1.5 text-gray-400 hover:text-gray-700 hover:bg-gray-100 rounded-xl transition"
          title="Go to Desk"
        >
          <span class="text-sm font-bold">↗</span>
          <span class="text-[9px] mt-0.5">Desk</span>
        </button>
      </div>
    </aside>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Top Header Bar -->
      <header class="bg-white border-b border-gray-200 px-4 py-2.5 flex items-center justify-between shadow-2xs z-20">
        <div class="flex items-center gap-2">
          <h2 class="text-base font-bold text-gray-900 capitalize">
            {{ currentTab === 'pos' ? 'Point of Sale' : currentTab === 'items' ? 'Item Catalogue' : currentTab === 'invoices' ? 'Sales Invoices' : 'Stock Entries' }}
          </h2>
          <span class="px-2 py-0.5 text-xs font-bold bg-blue-100 text-blue-700 rounded-md">Live</span>
        </div>

        <!-- Action Items -->
        <div class="flex items-center gap-2">
          <!-- POS Quick Add Brand & Item Buttons -->
          <button
            v-if="currentTab === 'pos' || currentTab === 'items'"
            @click="showCreateTemplateModal = true"
            class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-blue-50 hover:bg-blue-100 text-blue-700 flex items-center gap-1 transition shadow-2xs"
          >
            <span>+ Brand</span>
          </button>
          <button
            v-if="currentTab === 'pos' || currentTab === 'items'"
            @click="openVariantModal()"
            class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white flex items-center gap-1 transition shadow-xs"
          >
            <span>+ Item</span>
          </button>
          <button
            v-if="currentTab === 'pos'"
            @click="showAddCustomer = true"
            class="px-3 py-1.5 text-xs font-semibold rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700 flex items-center gap-1 transition"
          >
            <span>+ Customer</span>
          </button>
          <button
            @click="refreshCurrentTab"
            class="p-2 text-gray-500 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition"
            title="Refresh"
          >
            <svg class="w-4 h-4" :class="{'animate-spin': loading}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      </header>

      <!-- View 1: POS Screen -->
      <div v-show="currentTab === 'pos'" class="flex-1 flex overflow-hidden">
        <!-- Left Column: Items Selector with Filter Tabs -->
        <section class="flex-1 flex flex-col bg-gray-50 overflow-hidden border-r border-gray-200">
        <!-- Brand Items Capsule Bar -->
        <div class="px-3.5 py-2.5 bg-white border-b border-gray-200 flex items-center justify-between gap-2 overflow-x-auto scrollbar-none">
          <div class="flex items-center gap-2 overflow-x-auto scrollbar-none">
            <button
              @click="selectedTemplate = ''"
              :class="!selectedTemplate ? 'bg-blue-50 text-blue-600 border-2 border-blue-500 font-bold' : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'"
              class="px-3.5 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition shadow-xs"
            >
              All Brands
            </button>
            <button
              v-for="tmpl in templates"
              :key="tmpl.item_code"
              @click="selectedTemplate = tmpl.item_code"
              :class="selectedTemplate === tmpl.item_code ? 'bg-blue-50 text-blue-600 border-2 border-blue-500 font-bold' : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'"
              class="px-3.5 py-1.5 rounded-lg text-sm font-medium whitespace-nowrap transition shadow-xs"
            >
              {{ tmpl.item_name || tmpl.item_code }}
            </button>
          </div>

          <div class="flex items-center gap-1.5 flex-shrink-0">
            <button
              @click="showCreateTemplateModal = true"
              class="px-2.5 py-1 text-xs font-bold text-blue-600 hover:bg-blue-50 rounded-lg border border-dashed border-blue-300 transition flex items-center gap-1 whitespace-nowrap"
              title="Add New Brand"
            >
              <span>+ Brand</span>
            </button>
            <button
              @click="openVariantModal(selectedTemplate)"
              class="px-2.5 py-1 text-xs font-bold text-emerald-700 hover:bg-emerald-50 rounded-lg border border-dashed border-emerald-300 transition flex items-center gap-1 whitespace-nowrap"
              title="Add New Item"
            >
              <span>+ Item</span>
            </button>
          </div>
        </div>

        <!-- Search Bar with Instant Filter -->
        <div class="p-3 bg-white border-b border-gray-200">
          <div class="relative">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search by item code, name or barcode..."
              class="w-full bg-gray-50 border border-gray-200 rounded-xl pl-10 pr-8 py-2.5 text-sm focus:outline-none focus:bg-white focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition"
            />
            <span class="absolute left-3.5 top-3 text-gray-400">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </span>
            <button
              v-if="searchQuery"
              @click="searchQuery = ''"
              class="absolute right-3.5 top-2.5 text-gray-400 hover:text-gray-600 text-sm"
            >✕</button>
          </div>
        </div>

        <!-- Items Grid Cards (Dense, Compact Tiles with 14px Readable Standard Font) -->
        <div class="flex-1 overflow-y-auto p-3 content-start grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-2.5">
          <div
            v-for="item in filteredItems"
            :key="item.item_code"
            @click="addToCart(item)"
            :class="[
              'group relative rounded-xl p-2.5 touch-manipulation transition-all duration-100 h-20 self-start flex flex-col justify-between shadow-xs',
              item.is_stock_item && Number(item.actual_qty || 0) <= 0
                ? 'bg-gray-100/80 border border-gray-200 opacity-60 cursor-not-allowed'
                : 'bg-white border border-gray-200 hover:border-blue-500 hover:shadow-sm cursor-pointer active:scale-[0.98]'
            ]"
          >
            <!-- Available Qty Badge (Capsule: Green if in stock, Red if 0/out of stock) -->
            <div
              v-if="item.is_stock_item"
              :class="[
                'absolute -top-2 -end-2 inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-extrabold shadow-sm border-2 border-white select-none leading-tight',
                Number(item.actual_qty || 0) <= 0 ? 'bg-red-500 text-white' : 'bg-emerald-600 text-white'
              ]"
              :title="Number(item.actual_qty || 0) <= 0 ? 'Out of stock' : `Available Stock: ${item.actual_qty ?? 0}`"
            >
              <span
                class="w-1.5 h-1.5 rounded-full"
                :class="Number(item.actual_qty || 0) <= 0 ? 'bg-red-200' : 'bg-emerald-200 animate-pulse'"
              ></span>
              <span>{{ Math.floor(item.actual_qty ?? 0) }}</span>
            </div>

            <!-- Cart Count Badge (top-start if in cart) -->
            <div
              v-if="getItemCartQty(item.item_code)"
              class="absolute -top-1.5 -start-1.5 rounded-full shadow-xs z-10 w-5 h-5 flex items-center justify-center text-xs font-bold border border-white bg-blue-600 text-white select-none"
            >
              {{ getItemCartQty(item.item_code) }}
            </div>

            <!-- Item Header -->
            <div class="min-w-0">
              <h3
                class="text-sm font-bold text-gray-900 group-hover:text-blue-600 transition leading-snug truncate"
                :title="item.item_name || item.item_code"
              >
                {{ item.item_name || item.item_code }}
              </h3>
              <p class="text-xs text-gray-500 font-mono leading-tight truncate">
                {{ item.item_code }}
              </p>
            </div>

            <!-- Bottom Price & UOM -->
            <div class="pt-1 border-t border-gray-100 flex items-center justify-between text-xs leading-tight">
              <span class="text-gray-500 text-xs truncate">{{ item.stock_uom || 'Nos' }}</span>
              <span v-if="item.selling_price != null" class="font-extrabold text-blue-600 text-sm">
                ₹{{ Number(item.selling_price).toFixed(2) }}
              </span>
              <span v-else class="text-xs text-gray-400 italic">No price</span>
            </div>
          </div>

          <div v-if="filteredItems.length === 0" class="col-span-full h-48 flex flex-col items-center justify-center text-gray-400 text-sm">
            No items matching your search criteria
          </div>
        </div>
      </section>

      <!-- Right Column: Shopping Cart (Exact POS Next structure) -->
      <section class="w-[380px] bg-white flex flex-col shadow-xl z-20">
        <!-- Customer Selection Card (ERPNext POS Search & Select) -->
        <div class="p-3 border-b border-gray-200 bg-gray-50/70 relative">
          <!-- Selected Customer Card -->
          <div v-if="selectedCustomerDoc" class="flex items-center justify-between bg-white border border-gray-200 rounded-xl p-2.5 shadow-xs">
            <div class="flex items-center gap-2.5 min-w-0 flex-1">
              <div class="w-9 h-9 rounded-full bg-gradient-to-br from-blue-500 to-blue-600 text-white font-bold flex items-center justify-center text-sm flex-shrink-0 shadow-xs">
                {{ selectedCustomerDoc.customer_name?.charAt(0).toUpperCase() || 'C' }}
              </div>
              <div class="min-w-0 flex-1">
                <div class="text-sm font-bold text-gray-900 truncate">
                  {{ selectedCustomerDoc.customer_name }}
                </div>
                <div class="text-xs text-gray-500 truncate flex items-center gap-1.5 mt-0.5">
                  <span v-if="selectedCustomerDoc.mobile_no" class="text-blue-600 font-medium">📞 {{ selectedCustomerDoc.mobile_no }}</span>
                  <span v-else class="text-gray-400">No mobile</span>
                </div>
              </div>
            </div>

            <!-- Change Customer Button -->
            <button
              @click="toggleCustomerSearch"
              class="px-2.5 py-1 text-xs text-blue-600 hover:bg-blue-50 rounded-lg font-semibold transition"
            >
              Change
            </button>
          </div>

          <!-- Customer Live Search Field -->
          <div v-else class="relative">
            <div class="relative">
              <input
                v-model="customerSearchInput"
                @focus="isCustomerDropdownOpen = true"
                type="text"
                placeholder="Search by customer name or phone..."
                class="w-full bg-white border border-gray-300 rounded-xl pl-8 pr-20 py-2.5 text-sm font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 shadow-xs"
              />
              <span class="absolute left-2.5 top-2.5 text-gray-400 text-sm">👤</span>
              <button
                @click="showAddCustomer = true"
                class="absolute right-1.5 top-1.5 px-2.5 py-1.5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-lg transition"
              >
                + New
              </button>
            </div>

            <!-- Dropdown Results -->
            <div
              v-if="isCustomerDropdownOpen"
              class="absolute left-0 right-0 top-full mt-1 bg-white border border-gray-200 rounded-xl shadow-xl max-h-56 overflow-y-auto z-40 divide-y divide-gray-100"
            >
              <div
                v-for="c in searchedCustomers"
                :key="c.name"
                @click="selectCustomer(c)"
                class="p-2.5 hover:bg-blue-50/70 cursor-pointer transition flex items-center justify-between"
              >
                <div class="min-w-0 flex-1 pr-2">
                  <div class="text-sm font-bold text-gray-900 truncate">{{ c.customer_name || c.name }}</div>
                  <div class="text-xs text-gray-500 truncate flex items-center gap-2 mt-0.5">
                    <span v-if="c.mobile_no" class="text-blue-600 font-medium">📞 {{ c.mobile_no }}</span>
                    <span class="text-gray-400">{{ c.name }}</span>
                  </div>
                </div>
                <span class="text-xs text-blue-500 font-semibold">Select →</span>
              </div>

              <div v-if="searchedCustomers.length === 0" class="p-3 text-center text-xs text-gray-400">
                No customer found. Click <b>+ New</b> to create.
              </div>
            </div>
          </div>
        </div>

        <!-- Cart Items List -->
        <div class="flex-1 overflow-y-auto p-3 space-y-2">
          <div v-if="cart.length === 0" class="h-full flex flex-col items-center justify-center text-gray-400">
            <div class="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center text-xl mb-2 text-gray-400">
              🛒
            </div>
            <span class="text-sm font-bold text-gray-500">Cart is empty</span>
            <span class="text-xs text-gray-400 mt-0.5">Click any item from catalogue</span>
          </div>

          <div
            v-for="(row, idx) in cart"
            :key="idx"
            class="p-2.5 border border-gray-200 rounded-xl bg-gray-50/60 hover:bg-gray-50 flex items-center justify-between transition"
          >
            <div class="flex-1 min-w-0 pr-2">
              <div class="text-sm font-bold text-gray-900 truncate">{{ row.item_name }}</div>
              <div class="text-xs text-gray-500 mt-0.5">
                ₹{{ row.rate.toFixed(2) }} × {{ row.qty }} = <b class="text-gray-900 font-extrabold text-sm">₹{{ (row.rate * row.qty).toFixed(2) }}</b>
              </div>
            </div>

            <!-- Qty Stepper Controls -->
            <div class="flex items-center bg-white border border-gray-300 rounded-lg p-0.5 shadow-xs">
              <button
                @click.stop="decreaseQty(idx)"
                class="w-7 h-7 flex items-center justify-center text-gray-600 hover:bg-gray-100 rounded text-sm font-bold"
              >-</button>
              <span class="text-sm font-extrabold w-7 text-center text-gray-900">{{ row.qty }}</span>
              <button
                @click.stop="increaseQty(idx)"
                class="w-7 h-7 flex items-center justify-center text-gray-600 hover:bg-gray-100 rounded text-sm font-bold"
              >+</button>
            </div>
          </div>
        </div>

        <!-- Totals & Payment Section -->
        <div class="p-4 border-t border-gray-200 bg-gray-50 space-y-3">
          <!-- Quick Mode of Payment Tabs -->
          <div>
            <div class="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1.5">Payment Method</div>
            <div class="grid grid-cols-2 gap-2">
              <button
                v-for="m in paymentModes.slice(0, 4)"
                :key="m"
                @click="selectedPaymentMode = m"
                :class="selectedPaymentMode === m ? 'border-blue-600 bg-blue-50 text-blue-700 font-bold shadow-xs' : 'border-gray-200 bg-white text-gray-600 hover:bg-gray-100'"
                class="px-2.5 py-2 border rounded-lg text-sm text-center transition"
              >
                {{ m }}
              </button>
            </div>
          </div>

          <!-- Totals Breakdown -->
          <div class="border-t border-gray-200 pt-2.5 space-y-1">
            <div class="flex justify-between text-sm text-gray-500 font-medium">
              <span>Items Total ({{ totalQuantity }}):</span>
              <span>₹{{ subtotal.toFixed(2) }}</span>
            </div>
            <div class="flex justify-between text-base font-extrabold text-gray-900 pt-1 border-t border-dashed border-gray-200">
              <span>Grand Total:</span>
              <span class="text-blue-600 text-lg">₹{{ subtotal.toFixed(2) }}</span>
            </div>
          </div>

          <!-- Checkout Button -->
          <button
            @click="createInvoice"
            :disabled="cart.length === 0 || isSubmitting"
            class="w-full py-3 rounded-xl text-white font-extrabold text-sm bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 disabled:opacity-50 disabled:cursor-not-allowed shadow-md transition flex items-center justify-center gap-2 active:scale-[0.99]"
          >
            <span v-if="isSubmitting">Generating Invoice...</span>
            <span v-else>Pay & Print (₹{{ subtotal.toFixed(2) }})</span>
          </button>
        </div>
      </section>
    </div>

      <!-- View 1.5: Items Management Screen (Exact POS Cards Layout + Brand & Item Creator) -->
      <div v-show="currentTab === 'items'" class="flex-1 flex flex-col bg-gray-50 overflow-hidden">
        <!-- Top Toolbar & Brands Filter Bar -->
        <div class="px-4 py-2.5 bg-white border-b border-gray-200 flex items-center justify-between gap-3">
          <div class="flex items-center gap-2 overflow-x-auto scrollbar-none flex-1">
            <span class="text-xs font-bold text-gray-500 uppercase tracking-wider flex-shrink-0">Brands:</span>
            <button
              @click="itemsTabSelectedTemplate = ''"
              :class="!itemsTabSelectedTemplate ? 'bg-blue-50 text-blue-600 border-2 border-blue-500 font-bold' : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'"
              class="px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition shadow-xs"
            >
              All ({{ items.length }})
            </button>
            <button
              v-for="tmpl in templates"
              :key="tmpl.item_code"
              @click="itemsTabSelectedTemplate = tmpl.item_code"
              :class="itemsTabSelectedTemplate === tmpl.item_code ? 'bg-blue-50 text-blue-600 border-2 border-blue-500 font-bold' : 'bg-white text-gray-700 border border-gray-200 hover:bg-gray-50'"
              class="px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition shadow-xs flex items-center gap-1.5"
            >
              <span>{{ tmpl.item_name || tmpl.item_code }}</span>
            </button>
          </div>

          <!-- Live Filter Input -->
          <div class="w-64 relative flex-shrink-0">
            <input
              v-model="itemsSearchQuery"
              type="text"
              placeholder="Search items..."
              class="w-full bg-gray-50 border border-gray-200 rounded-xl pl-8 pr-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <span class="absolute left-2.5 top-2 text-gray-400 text-xs">🔍</span>
          </div>
        </div>

        <!-- Items Cards Grid (Same Compact & Readable Cards) -->
        <div class="flex-1 overflow-y-auto p-4 content-start grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-3">
          <div
            v-for="item in itemsTabFilteredList"
            :key="item.item_code"
            class="group relative bg-white border border-gray-200 hover:border-blue-500 rounded-xl p-2.5 transition-all shadow-xs hover:shadow-sm flex flex-col justify-between h-24 self-start"
          >
            <!-- Available Stock Badge -->
            <div
              v-if="item.is_stock_item"
              class="absolute -top-2 -end-2 inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-extrabold bg-emerald-600 text-white shadow-sm border-2 border-white select-none leading-tight"
            >
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-200"></span>
              <span>{{ Math.floor(item.actual_qty ?? 0) }}</span>
            </div>

            <!-- Item Info -->
            <div class="min-w-0">
              <span
                v-if="item.variant_of"
                class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200"
              >
                {{ item.variant_of }}
              </span>
              <h3 class="text-sm font-bold text-gray-900 truncate leading-snug mt-1" :title="item.item_name">
                {{ item.item_name || item.item_code }}
              </h3>
              <p class="text-xs text-gray-500 font-mono truncate">{{ item.item_code }}</p>
            </div>

            <!-- Price & Actions -->
            <div class="pt-1 border-t border-gray-100 flex items-center justify-between text-xs">
              <span class="text-gray-400">{{ item.stock_uom || 'Nos' }}</span>
              <span v-if="item.selling_price != null" class="font-extrabold text-blue-600 text-sm">
                ₹{{ Number(item.selling_price).toFixed(2) }}
              </span>
              <span v-else class="text-xs text-gray-400 italic">No price</span>
            </div>
          </div>

          <div v-if="itemsTabFilteredList.length === 0" class="col-span-full py-12 text-center text-gray-400 text-sm">
            No items found. Create a brand or add an item above.
          </div>
        </div>
      </div>

      <!-- View 2: Invoices List View -->
      <div v-show="currentTab === 'invoices'" class="flex-1 overflow-y-auto p-4 md:p-6 bg-gray-50">
        <div class="max-w-5xl mx-auto bg-white border border-gray-200 rounded-2xl shadow-xs overflow-hidden">
          <div class="p-4 border-b border-gray-200 flex items-center justify-between bg-gray-50/50">
            <div>
              <h3 class="text-base font-bold text-gray-900">Recent Invoices</h3>
              <p class="text-xs text-gray-500">Sales invoices created via POS and ERP</p>
            </div>
            <button
              @click="loadInvoices"
              class="px-3 py-1.5 text-xs font-semibold bg-white border border-gray-200 rounded-lg text-gray-700 hover:bg-gray-50"
            >
              Refresh Invoices
            </button>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead class="bg-gray-50 text-gray-600 font-semibold border-b border-gray-200 text-xs uppercase">
                <tr>
                  <th class="py-3 px-4">Invoice</th>
                  <th class="py-3 px-4">Customer</th>
                  <th class="py-3 px-4">Date</th>
                  <th class="py-3 px-4">Status</th>
                  <th class="py-3 px-4 text-right">Grand Total</th>
                  <th class="py-3 px-4 text-center">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="inv in invoices" :key="inv.name" class="hover:bg-blue-50/40 transition">
                  <td class="py-3 px-4 font-bold text-blue-600 font-mono">{{ inv.name }}</td>
                  <td class="py-3 px-4 font-medium text-gray-900">{{ inv.customer_name || inv.customer }}</td>
                  <td class="py-3 px-4 text-gray-500 text-xs">{{ inv.posting_date }}</td>
                  <td class="py-3 px-4">
                    <span
                      class="px-2 py-0.5 rounded text-xs font-bold"
                      :class="inv.status === 'Paid' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'"
                    >
                      {{ inv.status }}
                    </span>
                  </td>
                  <td class="py-3 px-4 text-right font-extrabold text-gray-900">₹{{ Number(inv.grand_total).toFixed(2) }}</td>
                  <td class="py-3 px-4 text-center">
                    <button
                      @click="printInvoice(inv.name)"
                      class="px-2.5 py-1 text-xs font-bold bg-blue-50 text-blue-700 hover:bg-blue-100 rounded-lg transition inline-flex items-center gap-1 shadow-2xs"
                      title="Print Invoice"
                    >
                      <span>🖨️</span>
                      <span>Print</span>
                    </button>
                  </td>
                </tr>
                <tr v-if="invoices.length === 0">
                  <td colspan="6" class="py-8 text-center text-gray-400">No invoices found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- View 3: Stock Entry List View -->
      <div v-show="currentTab === 'stock'" class="flex-1 overflow-y-auto p-4 md:p-6 bg-gray-50">
        <div class="max-w-5xl mx-auto bg-white border border-gray-200 rounded-2xl shadow-xs overflow-hidden">
          <div class="p-4 border-b border-gray-200 flex items-center justify-between bg-gray-50/50">
            <div>
              <h3 class="text-base font-bold text-gray-900">Stock Entries</h3>
              <p class="text-xs text-gray-500">Material receipts, issues, and manufacture transfers</p>
            </div>
            <div class="flex gap-2">
              <a
                href="/desk#Form/Stock Entry/new-stock-entry-1"
                class="px-3 py-1.5 text-xs font-bold bg-blue-600 hover:bg-blue-700 text-white rounded-lg shadow-xs"
              >
                + New Stock Entry
              </a>
              <button
                @click="loadStockEntries"
                class="px-3 py-1.5 text-xs font-semibold bg-white border border-gray-200 rounded-lg text-gray-700 hover:bg-gray-50"
              >
                Refresh
              </button>
            </div>
          </div>

          <div class="overflow-x-auto">
            <table class="w-full text-left text-sm">
              <thead class="bg-gray-50 text-gray-600 font-semibold border-b border-gray-200 text-xs uppercase">
                <tr>
                  <th class="py-3 px-4">Entry ID</th>
                  <th class="py-3 px-4">Purpose / Type</th>
                  <th class="py-3 px-4">Date</th>
                  <th class="py-3 px-4">Status</th>
                  <th class="py-3 px-4 text-right">Value</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="stk in stockEntries" :key="stk.name" class="hover:bg-blue-50/40 transition">
                  <td class="py-3 px-4 font-bold text-blue-600 font-mono">{{ stk.name }}</td>
                  <td class="py-3 px-4 font-medium text-gray-900">{{ stk.stock_entry_type || stk.purpose }}</td>
                  <td class="py-3 px-4 text-gray-500 text-xs">{{ stk.posting_date }}</td>
                  <td class="py-3 px-4">
                    <span
                      class="px-2 py-0.5 rounded text-xs font-bold"
                      :class="stk.docstatus === 1 ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'"
                    >
                      {{ stk.docstatus === 1 ? 'Submitted' : 'Draft' }}
                    </span>
                  </td>
                  <td class="py-3 px-4 text-right font-extrabold text-gray-900">₹{{ Number(stk.total_amount || 0).toFixed(2) }}</td>
                </tr>
                <tr v-if="stockEntries.length === 0">
                  <td colspan="5" class="py-8 text-center text-gray-400">No stock entries found</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Add Customer Modal -->
    <div
      v-if="showAddCustomer"
      class="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-5 space-y-4">
        <h2 class="text-sm font-bold text-gray-900">Add New Customer</h2>
        <div class="space-y-3">
          <div>
            <label class="text-[11px] font-semibold text-gray-600 block mb-1">Customer Name *</label>
            <input
              v-model="newCustomerName"
              type="text"
              placeholder="e.g. Ramesh Tailor"
              class="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="text-[11px] font-semibold text-gray-600 block mb-1">Mobile No</label>
            <input
              v-model="newCustomerMobile"
              type="text"
              placeholder="e.g. 9876543210"
              class="w-full border border-gray-300 rounded-lg px-3 py-1.5 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button
            @click="showAddCustomer = false"
            class="px-3 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
          >
            Cancel
          </button>
          <button
            @click="addNewCustomer"
            class="px-4 py-1.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-sm"
          >
            Save
          </button>
        </div>
      </div>
    </div>

    <!-- Create Brand / Template Item Modal -->
    <div
      v-if="showCreateTemplateModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-5 space-y-4">
        <div class="flex justify-between items-center border-b border-gray-100 pb-2">
          <h2 class="text-sm font-bold text-gray-900">Create Brand</h2>
          <button @click="showCreateTemplateModal = false" class="text-gray-400 hover:text-gray-600 text-sm">✕</button>
        </div>
        <p class="text-xs text-gray-500">Brands act as parent categories for all your items (e.g. Raymond, Kriplon, Siyaram).</p>
        <div class="space-y-3">
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Brand Name *</label>
            <input
              v-model="newTemplateName"
              type="text"
              placeholder="e.g. Raymond, Siyaram, Cotton-Fab"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Stock UOM</label>
            <select
              v-model="newTemplateUOM"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
            >
              <option value="Meter">Meter</option>
              <option value="Nos">Nos</option>
              <option value="Kg">Kg</option>
              <option value="Unit">Unit</option>
            </select>
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button
            @click="showCreateTemplateModal = false"
            class="px-3 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
          >
            Cancel
          </button>
          <button
            @click="submitCreateTemplate"
            :disabled="isSubmittingTemplate"
            class="px-4 py-1.5 text-xs font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-lg shadow-sm disabled:opacity-50"
          >
            <span v-if="isSubmittingTemplate">Creating...</span>
            <span v-else>Create Brand</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Create Item / Variant Modal -->
    <div
      v-if="showCreateVariantModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-sm p-5 space-y-4">
        <div class="flex justify-between items-center border-b border-gray-100 pb-2">
          <h2 class="text-sm font-bold text-gray-900">Add Item</h2>
          <button @click="showCreateVariantModal = false" class="text-gray-400 hover:text-gray-600 text-sm">✕</button>
        </div>

        <div class="space-y-3">
          <!-- Choose Brand: Existing or Create New -->
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Select Brand *</label>
            <div class="flex gap-1.5">
              <select
                v-model="newVariantTemplate"
                class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              >
                <option value="" disabled>Select brand...</option>
                <option v-for="t in templates" :key="t.item_code" :value="t.item_code">
                  {{ t.item_name || t.item_code }}
                </option>
              </select>
              <button
                @click="showCreateVariantModal = false; showCreateTemplateModal = true"
                class="px-2.5 py-2 text-xs font-bold text-blue-600 bg-blue-50 hover:bg-blue-100 rounded-lg whitespace-nowrap"
                title="Create a new brand"
              >
                + New Brand
              </button>
            </div>
          </div>

          <!-- Item Code/Identifier -->
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Item Code / Design No *</label>
            <input
              v-model="newVariantCode"
              type="text"
              placeholder="e.g. 004, Blue, 102"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <p v-if="newVariantTemplate && newVariantCode" class="text-[11px] text-gray-500 mt-1">
              Full Item Code: <b class="text-blue-600 font-mono">{{ newVariantTemplate }}-{{ newVariantCode }}</b>
            </p>
          </div>

          <!-- Selling Price -->
          <div>
            <label class="text-xs font-semibold text-gray-700 block mb-1">Selling Price (₹)</label>
            <input
              v-model="newVariantPrice"
              type="number"
              step="0.01"
              placeholder="e.g. 450.00"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>

        <div class="flex justify-end gap-2 pt-2">
          <button
            @click="showCreateVariantModal = false"
            class="px-3 py-1.5 text-xs text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
          >
            Cancel
          </button>
          <button
            @click="submitCreateVariant"
            :disabled="isSubmittingVariant || !newVariantTemplate || !newVariantCode"
            class="px-4 py-1.5 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm disabled:opacity-50"
          >
            <span v-if="isSubmittingVariant">Saving...</span>
            <span v-else>Save Item</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Success Dialog -->
    <div
      v-if="showSuccessDialog"
      class="fixed inset-0 bg-black/40 backdrop-blur-xs flex items-center justify-center z-50 p-4"
    >
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-md p-6 text-center space-y-4">
        <div class="w-12 h-12 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto text-2xl font-bold shadow-xs">
          ✓
        </div>
        <div>
          <h2 class="text-base font-bold text-gray-900">Invoice Created Successfully</h2>
          <p class="text-xs text-gray-500 mt-0.5">Submitted directly without POS Profile</p>
        </div>

        <div class="bg-gray-50 rounded-xl p-3 border border-gray-200 text-left text-xs space-y-1.5">
          <div class="flex justify-between">
            <span class="text-gray-500">Invoice No:</span>
            <span class="font-extrabold text-gray-900">{{ lastInvoice?.name }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Grand Total:</span>
            <span class="font-bold text-blue-600">₹{{ lastInvoice?.grand_total }}</span>
          </div>
          <div class="flex justify-between">
            <span class="text-gray-500">Status:</span>
            <span class="px-2 py-0.5 bg-green-100 text-green-700 font-bold rounded text-[10px]">{{ lastInvoice?.status }}</span>
          </div>
        </div>

        <div class="flex gap-2">
          <button
            v-if="lastInvoice?.name"
            @click="printInvoice(lastInvoice.name)"
            class="flex-1 py-2.5 bg-gray-100 hover:bg-gray-200 text-gray-800 font-bold rounded-xl transition flex items-center justify-center gap-1.5"
          >
            <span>🖨️</span>
            <span>Print Receipt</span>
          </button>
          <button
            @click="startNewSale"
            class="flex-1 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-md transition"
          >
            New Sale
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const currentTab = ref('pos');
const invoices = ref([]);
const stockEntries = ref([]);

// Items Tab State
const itemsTabSelectedTemplate = ref('');
const itemsSearchQuery = ref('');
const showCreateTemplateModal = ref(false);
const showCreateVariantModal = ref(false);
const isSubmittingTemplate = ref(false);
const isSubmittingVariant = ref(false);

const newTemplateName = ref('');
const newTemplateUOM = ref('Meter');
const newVariantTemplate = ref('');
const newVariantCode = ref('');
const newVariantPrice = ref('');

const searchQuery = ref('');
const customerSearchInput = ref('');
const isCustomerDropdownOpen = ref(false);
const selectedTemplate = ref('');
const loading = ref(false);
const isSubmitting = ref(false);
const showSuccessDialog = ref(false);
const showAddCustomer = ref(false);

const lastInvoice = ref(null);
const newCustomerName = ref('');
const newCustomerMobile = ref('');

const items = ref([]);
const templates = ref([]);
const customers = ref([]);
const paymentModes = ref(['Cash', 'UPI']);
const selectedCustomer = ref('');
const selectedPaymentMode = ref('Cash');
const cart = ref([]);

const selectedCustomerDoc = computed(() => {
  return customers.value.find((c) => c.name === selectedCustomer.value) || null;
});

const searchedCustomers = computed(() => {
  if (!customerSearchInput.value) return customers.value;
  const q = customerSearchInput.value.toLowerCase();
  return customers.value.filter(
    (c) =>
      (c.customer_name && c.customer_name.toLowerCase().includes(q)) ||
      (c.name && c.name.toLowerCase().includes(q)) ||
      (c.mobile_no && c.mobile_no.includes(q))
  );
});

function toggleCustomerSearch() {
  selectedCustomer.value = '';
  customerSearchInput.value = '';
  isCustomerDropdownOpen.value = true;
}

function selectCustomer(cust) {
  selectedCustomer.value = cust.name;
  isCustomerDropdownOpen.value = false;
  customerSearchInput.value = '';
}

const filteredItems = computed(() => {
  return items.value.filter((i) => {
    const matchesSearch =
      !searchQuery.value ||
      (i.item_name && i.item_name.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      (i.item_code && i.item_code.toLowerCase().includes(searchQuery.value.toLowerCase()));

    const matchesTemplate = !selectedTemplate.value || i.variant_of === selectedTemplate.value;

    return matchesSearch && matchesTemplate;
  });
});

const itemsTabFilteredList = computed(() => {
  return items.value.filter((i) => {
    const matchesSearch =
      !itemsSearchQuery.value ||
      (i.item_name && i.item_name.toLowerCase().includes(itemsSearchQuery.value.toLowerCase())) ||
      (i.item_code && i.item_code.toLowerCase().includes(itemsSearchQuery.value.toLowerCase()));

    const matchesTemplate = !itemsTabSelectedTemplate.value || i.variant_of === itemsTabSelectedTemplate.value;

    return matchesSearch && matchesTemplate;
  });
});

function openVariantModal(tmpl = '') {
  newVariantTemplate.value = tmpl || itemsTabSelectedTemplate.value || (templates.value[0]?.item_code || '');
  newVariantCode.value = '';
  newVariantPrice.value = '';
  showCreateVariantModal.value = true;
}

async function submitCreateTemplate() {
  if (!newTemplateName.value.trim()) {
    alert('Please enter template name');
    return;
  }
  isSubmittingTemplate.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.create_template_item', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({
        item_name: newTemplateName.value.trim(),
        stock_uom: newTemplateUOM.value || 'Meter',
      }),
    });
    const json = await res.json();
    if (json.message) {
      templates.value.unshift(json.message);
      itemsTabSelectedTemplate.value = json.message.item_code;
      showCreateTemplateModal.value = false;
      const createdTmpl = newTemplateName.value;
      newTemplateName.value = '';
      // Open variant creator immediately for ease
      openVariantModal(createdTmpl);
    } else {
      alert('Error creating template: ' + JSON.stringify(json._server_messages || json));
    }
  } catch (err) {
    alert('Failed to create template item');
  } finally {
    isSubmittingTemplate.value = false;
  }
}

async function submitCreateVariant() {
  if (!newVariantTemplate.value || !newVariantCode.value.trim()) {
    alert('Please choose template and variant suffix');
    return;
  }
  isSubmittingVariant.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.create_item_variant', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({
        template_item: newVariantTemplate.value,
        variant_code: newVariantCode.value.trim(),
        selling_price: newVariantPrice.value ? Number(newVariantPrice.value) : null,
      }),
    });
    const json = await res.json();
    if (json.message) {
      items.value.unshift(json.message);
      showCreateVariantModal.value = false;
      newVariantCode.value = '';
      newVariantPrice.value = '';
    } else {
      alert('Error creating variant: ' + JSON.stringify(json._server_messages || json));
    }
  } catch (err) {
    alert('Failed to create item variant');
  } finally {
    isSubmittingVariant.value = false;
  }
}

const subtotal = computed(() => {
  return cart.value.reduce((acc, row) => acc + row.qty * row.rate, 0);
});

const totalQuantity = computed(() => {
  return cart.value.reduce((acc, row) => acc + row.qty, 0);
});

const selectedCustomerName = computed(() => {
  const c = customers.value.find((c) => c.name === selectedCustomer.value);
  return c ? c.customer_name || c.name : 'Customer';
});

function getItemCartQty(item_code) {
  const row = cart.value.find((r) => r.item_code === item_code);
  return row ? row.qty : 0;
}

function getStockStatus(qty) {
  const quantity = Math.floor(qty !== undefined && qty !== null ? qty : 0);
  if (quantity <= 0) {
    return {
      color: 'bg-red-500',
      textColor: 'text-white',
    };
  }
  if (quantity <= 10) {
    return {
      color: 'bg-amber-500',
      textColor: 'text-white',
    };
  }
  return {
    color: 'bg-emerald-600',
    textColor: 'text-white',
  };
}

function addToCart(item) {
  if (item.is_stock_item && Number(item.actual_qty || 0) <= 0) {
    alert(`Item "${item.item_name || item.item_code}" is out of stock (Available: 0).`);
    return;
  }
  if (item.selling_price == null) {
    alert(`Item ${item.item_code} does not have an active selling price.`);
    return;
  }
  const existing = cart.value.find((r) => r.item_code === item.item_code);
  if (existing) {
    if (item.is_stock_item && existing.qty >= Number(item.actual_qty || 0)) {
      alert(`Cannot add more than available stock (${item.actual_qty}).`);
      return;
    }
    existing.qty += 1;
  } else {
    cart.value.push({
      item_code: item.item_code,
      item_name: item.item_name || item.item_code,
      rate: Number(item.selling_price) || 0,
      qty: 1,
    });
  }
}

function increaseQty(idx) {
  const row = cart.value[idx];
  const itemDoc = items.value.find((i) => i.item_code === row.item_code);
  if (itemDoc && itemDoc.is_stock_item && row.qty >= Number(itemDoc.actual_qty || 0)) {
    alert(`Cannot exceed available stock (${itemDoc.actual_qty}).`);
    return;
  }
  row.qty += 1;
}

function decreaseQty(idx) {
  if (cart.value[idx].qty > 1) {
    cart.value[idx].qty -= 1;
  } else {
    cart.value.splice(idx, 1);
  }
}

async function loadData() {
  loading.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_pos_data', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
    });
    const json = await res.json();
    if (json.message) {
      items.value = json.message.items || [];
      templates.value = json.message.templates || [];
      customers.value = json.message.customers || [];
      paymentModes.value = json.message.modes_of_payment || ['Cash', 'UPI'];
      if (!selectedPaymentMode.value && paymentModes.value.length) {
        selectedPaymentMode.value = paymentModes.value[0];
      }
    }
  } catch (err) {
    console.error('Failed to load POS data', err);
  } finally {
    loading.value = false;
  }
}

async function addNewCustomer() {
  if (!newCustomerName.value) {
    alert('Customer name is required');
    return;
  }
  try {
    const res = await fetch('/api/method/tailorms.api.create_customer', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify({
        customer_name: newCustomerName.value,
        mobile_no: newCustomerMobile.value,
      }),
    });
    const json = await res.json();
    if (json.message) {
      customers.value.unshift(json.message);
      selectedCustomer.value = json.message.name;
      newCustomerName.value = '';
      newCustomerMobile.value = '';
      showAddCustomer.value = false;
    }
  } catch (err) {
    alert('Failed to create customer');
  }
}

async function createInvoice() {
  if (!selectedCustomer.value) {
    alert('Please select a customer.');
    return;
  }
  if (cart.value.length === 0) return;

  isSubmitting.value = true;
  try {
    const payload = {
      customer: selectedCustomer.value,
      items: cart.value.map((r) => ({
        item_code: r.item_code,
        qty: r.qty,
        rate: r.rate,
      })),
      payments: [
        {
          mode_of_payment: selectedPaymentMode.value || 'Cash',
          amount: subtotal.value,
        },
      ],
      update_stock: 0,
    };

    const res = await fetch('/api/method/tailorms.api.create_sales_invoice', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
      body: JSON.stringify(payload),
    });

    const json = await res.json();
    if (json.message && json.message.name) {
      lastInvoice.value = json.message;
      showSuccessDialog.value = true;
      cart.value = [];
    } else {
      alert('Error creating invoice: ' + JSON.stringify(json._server_messages || json));
    }
  } catch (err) {
    alert('Network error while creating invoice');
    console.error(err);
  } finally {
    isSubmitting.value = false;
  }
}

function goToDesk() {
  window.location.href = '/desk';
}

function startNewSale() {
  showSuccessDialog.value = false;
  cart.value = [];
  selectedCustomer.value = '';
  customerSearchInput.value = '';
  searchQuery.value = '';
  selectedTemplate.value = '';
  selectedPaymentMode.value = paymentModes.value[0] || 'Cash';
  lastInvoice.value = null;
  loadData();
}

function printInvoice(invoiceName) {
  if (!invoiceName) return;
  const printUrl = `/printview?doctype=Sales+Invoice&name=${encodeURIComponent(invoiceName)}&format=Standard&no_letterhead=0&letterhead=No+Letterhead`;
  window.open(printUrl, '_blank');
}

async function loadInvoices() {
  loading.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_invoices', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
    });
    const json = await res.json();
    if (json.message) {
      invoices.value = json.message || [];
    }
  } catch (err) {
    console.error('Failed to load invoices', err);
  } finally {
    loading.value = false;
  }
}

async function loadStockEntries() {
  loading.value = true;
  try {
    const res = await fetch('/api/method/tailorms.api.get_stock_entries', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': window.csrf_token || '',
      },
    });
    const json = await res.json();
    if (json.message) {
      stockEntries.value = json.message || [];
    }
  } catch (err) {
    console.error('Failed to load stock entries', err);
  } finally {
    loading.value = false;
  }
}

function switchTab(tab) {
  currentTab.value = tab;
  if (tab === 'invoices') {
    loadInvoices();
  } else if (tab === 'stock') {
    loadStockEntries();
  }
}

function refreshCurrentTab() {
  if (currentTab.value === 'pos') {
    loadData();
  } else if (currentTab.value === 'invoices') {
    loadInvoices();
  } else if (currentTab.value === 'stock') {
    loadStockEntries();
  }
}

onMounted(() => {
  loadData();
});
</script>

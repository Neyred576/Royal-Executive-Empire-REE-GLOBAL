import os

admin_path = r"C:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\DIVISIONS WEBSITE\REEL TECH HUB\Main\REEL Tech Hub\src\pages\Admin.tsx"

with open(admin_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add body scroll lock effect
target_auth = """  useEffect(() => {
    const authStatus = sessionStorage.getItem(AUTH_STORAGE_KEY);
    if (authStatus === "true") {
      setIsAuthenticated(true);
      setProducts(getStoredProducts());
    }
  }, []);"""

replacement_auth = """  useEffect(() => {
    const authStatus = sessionStorage.getItem(AUTH_STORAGE_KEY);
    if (authStatus === "true") {
      setIsAuthenticated(true);
      setProducts(getStoredProducts());
    }
  }, []);

  // Lock body scroll when modal is open
  useEffect(() => {
    if (isFormOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isFormOpen]);"""

if target_auth in content:
    content = content.replace(target_auth, replacement_auth, 1)
    print("Added body scroll lock effect")
else:
    print("target_auth not found")

# 2. Fix the modal structure
target_modal_start = """      {/* ==================== 3. PRODUCT PUBLISH / EDIT MODAL ==================== */}
      <AnimatePresence>
        {isFormOpen && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/80 backdrop-blur-md overflow-y-auto">
            <motion.div
              initial={{ opacity: 0, scale: 0.95, y: 20 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.95, y: 20 }}
              className="w-full max-w-2xl bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl overflow-hidden my-8"
            >
              {/* Modal Header */}
              <div className="px-6 py-4 border-b border-zinc-800 flex items-center justify-between">
                <div>
                  <h3 className="text-base font-semibold text-white">
                    {editingId ? "Edit Product Details" : "Publish New Store Product"}
                  </h3>
                  <p className="text-xs text-zinc-400">
                    Product appears instantly in the REEL Tech Hub store upon saving.
                  </p>
                </div>
                <button
                  onClick={() => setIsFormOpen(false)}
                  className="p-1 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Modal Form */}
              <form onSubmit={handleSaveProduct} className="p-6 space-y-5">"""

replacement_modal_start = """      {/* ==================== 3. PRODUCT PUBLISH / EDIT MODAL ==================== */}
      <AnimatePresence>
        {isFormOpen && (
          <div
            className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/85 backdrop-blur-md"
            onClick={(e) => {
              if (e.target === e.currentTarget) setIsFormOpen(false);
            }}
          >
            <motion.div
              initial={{ opacity: 0, scale: 0.96, y: 15 }}
              animate={{ opacity: 1, scale: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.96, y: 15 }}
              className="w-full max-w-2xl max-h-[90vh] bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl flex flex-col overflow-hidden my-auto"
            >
              {/* Modal Header (Pinned at top) */}
              <div className="px-6 py-4 border-b border-zinc-800 flex items-center justify-between shrink-0 bg-zinc-900 z-10">
                <div>
                  <h3 className="text-base font-semibold text-white">
                    {editingId ? "Edit Product Details" : "Publish New Store Product"}
                  </h3>
                  <p className="text-xs text-zinc-400">
                    Product appears instantly in the REEL Tech Hub store upon saving.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => setIsFormOpen(false)}
                  className="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {/* Modal Form with Scrollable Content Body & Sticky Footer */}
              <form onSubmit={handleSaveProduct} className="flex flex-col flex-1 min-h-0 overflow-hidden">
                <div className="p-6 space-y-5 overflow-y-auto flex-1">"""

if target_modal_start in content:
    content = content.replace(target_modal_start, replacement_modal_start, 1)
    print("Replaced modal start")
else:
    print("target_modal_start not found")

# 3. Fix the modal end (wrap inputs div and pin footer)
target_modal_end = """                <div className="pt-4 border-t border-zinc-800 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="status-publish"
                      checked={formData.status === "published"}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          status: e.target.checked ? "published" : "draft",
                        })
                      }
                      className="rounded bg-zinc-950 border-zinc-700"
                    />
                    <label htmlFor="status-publish" className="text-xs text-zinc-300 cursor-pointer">
                      Publish live on website immediately
                    </label>
                  </div>

                  <div className="flex items-center gap-3">
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => setIsFormOpen(false)}
                      className="text-xs text-zinc-400"
                    >
                      Cancel
                    </Button>
                    <Button
                      type="submit"
                      size="sm"
                      className="bg-white text-black hover:bg-zinc-200 text-xs font-semibold px-6 py-2"
                    >
                      {editingId ? "Save Changes" : "Publish Product"}
                    </Button>
                  </div>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>"""

replacement_modal_end = """                </div>

                {/* Modal Footer (Pinned at bottom) */}
                <div className="p-4 px-6 border-t border-zinc-800 flex items-center justify-between shrink-0 bg-zinc-900/95 backdrop-blur-sm z-10">
                  <div className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      id="status-publish"
                      checked={formData.status === "published"}
                      onChange={(e) =>
                        setFormData({
                          ...formData,
                          status: e.target.checked ? "published" : "draft",
                        })
                      }
                      className="rounded bg-zinc-950 border-zinc-700"
                    />
                    <label htmlFor="status-publish" className="text-xs text-zinc-300 cursor-pointer">
                      Publish live on website immediately
                    </label>
                  </div>

                  <div className="flex items-center gap-3">
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      onClick={() => setIsFormOpen(false)}
                      className="text-xs text-zinc-400"
                    >
                      Cancel
                    </Button>
                    <Button
                      type="submit"
                      size="sm"
                      className="bg-white text-black hover:bg-zinc-200 text-xs font-semibold px-6 py-2"
                    >
                      {editingId ? "Save Changes" : "Publish Product"}
                    </Button>
                  </div>
                </div>
              </form>
            </motion.div>
          </div>
        )}
      </AnimatePresence>"""

if target_modal_end in content:
    content = content.replace(target_modal_end, replacement_modal_end, 1)
    print("Replaced modal end")
else:
    print("target_modal_end not found")

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(content)
print("Admin.tsx successfully updated!")


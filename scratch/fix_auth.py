auth_path = r"C:\Users\prosp\Desktop\WEBSITES\Royal Exercutive Empire\DIVISIONS WEBSITE\REEL TECH HUB\Main\REEL Tech Hub\src\pages\Auth.tsx"

with open(auth_path, "r", encoding="utf-8") as f:
    c = f.read()

# Replace import of Tent with reelLogo and ShieldCheck
c = c.replace('import { Tent, ArrowLeft } from "lucide-react";', 'import { ArrowLeft, ShieldCheck } from "lucide-react";\nimport reelLogo from "@/assets/reel-logo.png";')

# Replace Wild Haven header
old_header = """        <div className="text-center mb-10">
          <div className="flex items-center justify-center gap-2 mb-6">
            <Tent className="h-5 w-5 text-primary" />
            <span className="text-sm font-normal tracking-wide text-background">
              Wild Haven
            </span>
          </div>
          <h1 className="text-2xl font-light text-background mb-2 tracking-tight">
            {isLogin ? "Admin Login" : "Create Account"}
          </h1>
          <p className="text-xs text-background/60 font-light">
            {isLogin
              ? "Sign in to manage your properties"
              : "Register for admin access"}
          </p>
        </div>"""

new_header = """        <div className="text-center mb-8">
          <img
            src={reelLogo}
            alt="REEL Tech Hub Logo"
            className="h-14 w-auto mx-auto mb-3 object-contain"
          />
          <h1 className="text-xl font-semibold text-background mb-1 tracking-wider uppercase">
            REEL TECH HUB
          </h1>
          <p className="text-xs text-background/60">
            {isLogin
              ? "Sign in to access publishing console"
              : "Register for admin access"}
          </p>
        </div>"""

c = c.replace(old_header, new_header)

# Replace placeholder admin@wildhaven.com
c = c.replace('placeholder="admin@wildhaven.com"', 'placeholder="admin@reelholding.com.ng"')

# Add link to /admin at bottom
old_footer = """        <div className="mt-8 text-center">
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="text-xs text-background/50 hover:text-background/80 font-light transition-colors"
          >
            {isLogin ? "Need an account? Sign up" : "Already have an account? Sign in"}
          </button>
        </div>"""

new_footer = """        <div className="mt-6 text-center space-y-3">
          <button
            onClick={() => setIsLogin(!isLogin)}
            className="text-xs text-background/50 hover:text-background/80 font-light transition-colors block mx-auto"
          >
            {isLogin ? "Need an account? Sign up" : "Already have an account? Sign in"}
          </button>

          <div className="pt-4 border-t border-background/20 space-y-2">
            <button
              type="button"
              onClick={() => navigate("/admin")}
              className="text-xs text-primary hover:underline font-medium inline-flex items-center gap-1.5"
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              Administrator Key Login (/admin)
            </button>
            <div>
              <button
                type="button"
                onClick={() => navigate("/")}
                className="text-xs text-background/50 hover:text-background/80 transition-colors inline-flex items-center gap-1"
              >
                <ArrowLeft className="w-3 h-3" />
                Back to REEL Tech Hub
              </button>
            </div>
          </div>
        </div>"""

c = c.replace(old_footer, new_footer)

with open(auth_path, "w", encoding="utf-8") as f:
    f.write(c)

print("Auth.tsx successfully updated!")


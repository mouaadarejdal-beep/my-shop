import os

# --- CONFIGURATION ---
BASE_DIR = os.getcwd()
NETLIFY_CONFIG_FILE = os.path.join(BASE_DIR, "netlify.toml")

def create_netlify_config():
    print("--- Creating Netlify Configuration ---")
    
    # This file tells Netlify EXACTLY which version of Hugo to install
    # and what command to run.
    toml_content = """
[build]
  publish = "public"
  command = "hugo --gc --minify"

[build.environment]
  HUGO_VERSION = "0.120.4"
  HUGO_ENV = "production"
  # This setting ensures Netlify installs the 'extended' version of Hugo (needed for designs)
  HUGO_EXTENDED = "true"

[context.production.environment]
  HUGO_ENV = "production"

[context.deploy-preview]
  command = "hugo --gc --minify -b $DEPLOY_PRIME_URL"

[context.branch-deploy]
  command = "hugo --gc --minify -b $DEPLOY_PRIME_URL"
"""
    
    with open(NETLIFY_CONFIG_FILE, "w", encoding="utf-8") as f:
        f.write(toml_content)
        
    print("✅ 'netlify.toml' created successfully.")
    print("------------------------------------------------")
    print("👉 NEXT STEPS (Do this now):")
    print("1. Open GitHub Desktop.")
    print("2. You will see 'netlify.toml' as a new file.")
    print("3. Type 'Fix Netlify Build' in the summary.")
    print("4. Click 'Commit' -> 'Push origin'.")
    print("------------------------------------------------")

if __name__ == "__main__":
    create_netlify_config()
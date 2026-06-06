#!/usr/bin/env python3
import os
import sys
import re
import shutil
import zipfile
import argparse
from html.parser import HTMLParser

class AuraHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = []
        self.classes_found = set()
        self.style_rules = {}
        self.inline_style_counter = 0
        self.tag_stack = []

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        attrs_dict = dict(attrs)
        
        # Strip Aura-specific editor attributes
        cleaned_attrs = []
        element_classes = []
        inline_style = None

        for name, value in attrs:
            if name.startswith('data-aura-') or name.startswith('data-arcade-'):
                continue
            if name == 'class':
                element_classes = [c for c in value.split() if c]
                # Save classes for SCSS generation
                for c in element_classes:
                    self.classes_found.add(c)
            elif name == 'style':
                inline_style = value
                continue
            cleaned_attrs.append((name, value))

        # Handle inline styles in SCSS mode
        if inline_style:
            self.inline_style_counter += 1
            # Find or create a semantic class name if none exists
            cls_name = None
            for name, val in cleaned_attrs:
                if name == 'class':
                    cls_name = val.split()[0] if val.split() else f"style-ref-{self.inline_style_counter}"
                    break
            if not cls_name:
                cls_name = f"style-ref-{self.inline_style_counter}"
                cleaned_attrs.append(('class', cls_name))
                element_classes.append(cls_name)
            
            # Save style rules for SCSS output
            self.style_rules[cls_name] = inline_style

        # Reconstruct the tag
        attr_str = ""
        if cleaned_attrs:
            attr_str = " " + " ".join(f'{name}="{value}"' if value is not None else name for name, value in cleaned_attrs)
        
        self.output.append(f"<{tag}{attr_str}>")

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        self.output.append(f"</{tag}>")

    def handle_data(self, data):
        self.output.append(data)

    def handle_comment(self, data):
        # Ignore Aura-specific editor comments
        if "aura" in data.lower() or "arcade" in data.lower() or "editor" in data.lower():
            return
        self.output.append(f"<!--{data}-->")

    def handle_entityref(self, name):
        self.output.append(f"&{name};")

    def handle_charref(self, name):
        self.output.append(f"&#{name};")

    def get_cleaned_html(self):
        return "".join(self.output)


def clean_html_content(raw_html, mode="tailwind"):
    # Pre-strip script tags that belong to Aura editor or tracking
    # We want to keep standard CDNs or animations scripts if they aren't Aura components
    def script_filter(match):
        script_content = match.group(0)
        if any(term in script_content.lower() for term in ["or.build", "aura.build", "arcade", "editor-widget", "hotjar", "google-analytics"]):
            return "" # Strip
        return script_content

    cleaned_raw = re.sub(r'<script\b[^>]*>([\s\S]*?)<\/script>', script_filter, raw_html)
    
    # Run HTML parser
    parser = AuraHTMLParser()
    parser.feed(cleaned_raw)
    cleaned_html = parser.get_cleaned_html()

    # Post-clean: format output
    # If SCSS mode, we will also return the generated SCSS content
    scss_content = ""
    if mode == "scss" and (parser.classes_found or parser.style_rules):
        scss_content = "/* Styles générés automatiquement par Aura.build Assistant */\n\n"
        
        # 1. Add inline styles converted to classes
        if parser.style_rules:
            scss_content += "/* Styles inline extraits */\n"
            for cls_name, rule in parser.style_rules.items():
                # Format style rules for SCSS
                formatted_rule = "  " + ";\n  ".join([r.strip() for r in rule.split(';') if r.strip()])
                if not formatted_rule.endswith('\n  '):
                    formatted_rule += ";\n"
                scss_content += f".{cls_name} {{\n{formatted_rule}}}\n\n"
        
        # 2. Add classes skeleton
        scss_content += "/* Structure des classes */\n"
        # We group Tailwind utility classes vs custom class names if possible
        # For simplicity, we create empty rules for custom classes (non-Tailwind-looking)
        # Tailwind classes typically have colons, dashes with numbers, or are short util names.
        custom_classes = []
        tailwind_classes = []
        for c in sorted(parser.classes_found):
            # Simple heuristic for custom vs tailwind classes
            if c in parser.style_rules:
                continue
            is_tailwind = any(char in c for char in [':', '/']) or any(c.startswith(p) for p in ['w-', 'h-', 'p-', 'm-', 'bg-', 'text-', 'flex', 'grid', 'border-', 'rounded-', 'shadow-', 'opacity-', 'cursor-', 'transition-', 'duration-', 'ease-', 'absolute', 'relative', 'fixed', 'top-', 'bottom-', 'left-', 'right-', 'z-', 'justify-', 'items-', 'self-'])
            if is_tailwind:
                tailwind_classes.append(c)
            else:
                custom_classes.append(c)

        if custom_classes:
            for c in custom_classes:
                scss_content += f".{c} {{\n  /* À compléter */\n}}\n\n"
        
        if tailwind_classes:
            scss_content += "/* Classes Tailwind détectées :\n"
            for c in tailwind_classes:
                scss_content += f"   .{c}\n"
            scss_content += "*/\n"

    return cleaned_html, scss_content


def process_file(file_path, mode, output_base_dir):
    filename = os.path.basename(file_path)
    basename, ext = os.path.splitext(filename)
    comp_output_dir = os.path.join(output_base_dir, basename)
    os.makedirs(comp_output_dir, exist_ok=True)

    print(f"[*] Traitement du fichier : {filename}")
    print(f"[*] Mode cible : {mode}")
    print(f"[*] Dossier de staging : {comp_output_dir}")

    html_files_processed = 0

    if ext.lower() == '.zip':
        # Temporary extraction directory
        temp_extract_dir = os.path.join(output_base_dir, f"_temp_{basename}")
        os.makedirs(temp_extract_dir, exist_ok=True)
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extract_dir)
            
            # Walk and process all html files
            for root, _, files in os.walk(temp_extract_dir):
                for f in files:
                    f_path = os.path.join(root, f)
                    f_ext = os.path.splitext(f)[1].lower()
                    rel_dir = os.path.relpath(root, temp_extract_dir)
                    dest_dir = comp_output_dir if rel_dir == '.' else os.path.join(comp_output_dir, rel_dir)
                    os.makedirs(dest_dir, exist_ok=True)

                    if f_ext == '.html':
                        with open(f_path, 'r', encoding='utf-8', errors='ignore') as html_file:
                            content = html_file.read()
                        
                        cleaned_html, scss_content = clean_html_content(content, mode)
                        
                        # Save HTML
                        dest_html_path = os.path.join(dest_dir, f)
                        with open(dest_html_path, 'w', encoding='utf-8') as out_file:
                            out_file.write(cleaned_html)
                        print(f"    [+] HTML nettoyé généré : {os.path.relpath(dest_html_path)}")

                        # Save SCSS if mode matches
                        if mode == "scss" and scss_content:
                            scss_filename = os.path.splitext(f)[0] + ".scss"
                            dest_scss_path = os.path.join(dest_dir, scss_filename)
                            with open(dest_scss_path, 'w', encoding='utf-8') as out_file:
                                out_file.write(scss_content)
                            print(f"    [+] SCSS généré : {os.path.relpath(dest_scss_path)}")
                        
                        html_files_processed += 1
                    else:
                        # Copy other assets directly
                        dest_asset_path = os.path.join(dest_dir, f)
                        shutil.copy2(f_path, dest_asset_path)
                        print(f"    [+] Asset copié : {os.path.relpath(dest_asset_path)}")

        finally:
            # Clean up temp extraction folder
            shutil.rmtree(temp_extract_dir, ignore_errors=True)

    elif ext.lower() == '.html':
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as html_file:
            content = html_file.read()

        cleaned_html, scss_content = clean_html_content(content, mode)

        # Save HTML
        dest_html_path = os.path.join(comp_output_dir, filename)
        with open(dest_html_path, 'w', encoding='utf-8') as out_file:
            out_file.write(cleaned_html)
        print(f"    [+] HTML nettoyé généré : {os.path.relpath(dest_html_path)}")

        # Save SCSS
        if mode == "scss" and scss_content:
            dest_scss_path = os.path.join(comp_output_dir, f"{basename}.scss")
            with open(dest_scss_path, 'w', encoding='utf-8') as out_file:
                out_file.write(scss_content)
            print(f"    [+] SCSS généré : {os.path.relpath(dest_scss_path)}")
        
        html_files_processed += 1
    else:
        print(f"[!] Format de fichier non supporté : {ext}")
        return False

    # Clean up the original file from imports directory
    try:
        os.remove(file_path)
        print(f"[*] Fichier d'origine supprimé : {filename}")
    except Exception as e:
        print(f"[!] Impossible de supprimer le fichier d'origine : {e}")

    print(f"[✓] Importation réussie ! {html_files_processed} page(s) traitée(s).\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="Nettoie et convertit les exports de code d'Aura.build.")
    parser.add_argument('--file', help="Nom du fichier .html ou .zip dans le dossier ./aura-imports/")
    parser.add_argument('--mode', choices=['tailwind', 'scss'], default='tailwind', help="Mode d'import : tailwind ou scss")
    
    args = parser.parse_args()

    # Setup directories relative to current working directory
    workspace_dir = os.getcwd()
    imports_dir = os.path.join(workspace_dir, "aura-imports")
    output_dir = os.path.join(imports_dir, "output")

    os.makedirs(imports_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # If no file is specified, scan the imports directory
    file_to_process = None
    if args.file:
        full_path = os.path.join(imports_dir, args.file)
        if os.path.exists(full_path):
            file_to_process = full_path
        else:
            print(f"[!] Le fichier spécifié n'existe pas : {full_path}")
            sys.exit(1)
    else:
        # Scan imports_dir for the first .html or .zip file (ignoring output directory and hidden files)
        for entry in os.listdir(imports_dir):
            entry_path = os.path.join(imports_dir, entry)
            if os.path.isfile(entry_path) and not entry.startswith('.'):
                ext = os.path.splitext(entry)[1].lower()
                if ext in ['.html', '.zip']:
                    file_to_process = entry_path
                    break

    if not file_to_process:
        print(f"[!] Aucun fichier .html ou .zip trouvé dans {imports_dir}.")
        print("[*] Veuillez y déposer un fichier avant de relancer l'importation.")
        sys.exit(1)

    success = process_file(file_to_process, args.mode, output_dir)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()

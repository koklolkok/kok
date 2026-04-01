# Requirements: pip install requests beautifulsoup4
import os
import random
import string
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
import urllib.parse
import time

# ==============================================================================
# GENERATOR PRO - ULTIMATE SPIDER & GOOGLE FRESHNESS SYNC (V4.5)
# - تم التحديث لدعم القوالب: test.html, test1.html, test2.html
# - اختيار عشوائي للقوالب لضمان تنوع المحتوى أمام محركات البحث.
# ==============================================================================

class ContinuousGenerator:
    def __init__(self):
        self.templates = {}
        # تم إضافة test1.html و test2.html إلى قائمة القوالب المدعومة
        self.template_names = ["test.html", "test1.html", "test2.html"]
        self.phrases_global = []
        self.emojis = ["🔥", "🎥", "🔞", "😱", "✅", "🌟", "📺", "🎬", "✨", "💎", "⚡", "🍭", "🍇", "🧿", "👑", "🚀", "💥", "🔴"]
        self.band_file = "band.txt"
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }

        self.languages = [
            "Arabic", "English", "Spanish", "French", "German", 
            "Italian", "Russian", "Japanese", "Chinese", "Hindi", 
            "Portuguese", "Turkish", "Korean", "Vietnamese", "Thai", 
            "Dutch", "Polish", "Indonesian", "Malay", "Persian"
        ]
        
        self.multi_lang_sources = {
            "Arabic": ["https://www.sexnyk.com/", "https://www.aflamsex69.com/", "https://zebawy.com/", "https://www.asax.tv/"],
            "English": ["https://www.pornhub.com/", "https://www.youporn.com/", "https://www.redtube.com/", "https://www.xhamster.com/"],
            "Spanish": ["https://es.pornhub.com/", "https://www.xvideos.com/spanish/"],
            "French": ["https://fr.pornhub.com/", "https://www.xvideos.com/french/"],
            "German": ["https://de.pornhub.com/", "https://www.xvideos.com/german/"],
            "Russian": ["https://rt.pornhub.com/", "https://www.xvideos.com/russian/"],
            "Japanese": ["https://jp.pornhub.com/", "https://www.xvideos.com/japanese/"],
            "Chinese": ["https://cn.pornhub.com/", "https://www.xvideos.com/chinese/", "https://www.t66y.com/"],
            "Turkish": ["https://tr.pornhub.com/", "https://www.xvideos.com/turkish/"]
        }

        self.searched_history = self.load_band_list()
        self.load_all_templates()
        self.smart_global_crawler(max_iters_per_lang=3)

    def load_band_list(self):
        if not os.path.exists(self.band_file): return set()
        try:
            with open(self.band_file, "r", encoding="utf-8") as f:
                return set([line.strip() for line in f if line.strip()])
        except: return set()

    def save_to_band_list(self, word):
        try:
            with open(self.band_file, "a", encoding="utf-8") as f:
                f.write(f"{word}\n")
        except: pass

    def load_all_templates(self):
        """تحميل محتوى جميع القوالب المحددة في القائمة"""
        for t_name in self.template_names:
            if os.path.exists(t_name):
                try:
                    with open(t_name, "r", encoding="utf-8") as f:
                        self.templates[t_name] = f.read()
                        print(f"[*] Template {t_name} loaded successfully.")
                except Exception as e:
                    print(f"[!] Error loading {t_name}: {e}")
            else:
                # إنشاء قالب افتراضي في حال عدم وجود الملف الفيزيائي
                self.templates[t_name] = """
                <!DOCTYPE html><html lang="en"><head>
                <meta charset="utf-8"/><title>{{TITLE}}</title>
                <meta property="article:published_time" content="{{DATE}}"/>
                <meta property="og:updated_time" content="{{DATE}}"/>
                </head><body>
                <h1>{{TITLE}}</h1><p>{{DESCRIPTION}}</p>
                <div class="content">{{INTERNAL_LINKS}}</div>
                <time datetime="{{DATE}}">{{DATE_SQL}}</time>
                </body></html>
                """

    def dynamic_extract_keywords(self, text, lang):
        if lang == "Arabic" or lang == "Persian":
            words = re.findall(r'[\u0600-\u06FF]+', text)
        elif any(l in lang for l in ["Japanese", "Chinese", "Korean", "Thai"]):
            words = re.findall(r'[\u4e00-\u9fff\u3040-\u309f\uac00-\ud7af\u0e00-\u0e7f]{2,}', text)
        else:
            words = re.findall(r'[a-zA-Z]{4,}', text)
        return [w for w in words if len(w) >= 3]

    def get_initial_keywords_from_home(self, url, lang):
        try:
            res = requests.get(url, headers=self.headers, timeout=5)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                keywords = self.dynamic_extract_keywords(soup.get_text(), lang)
                if keywords: return random.sample(keywords, min(len(keywords), 10))
        except: pass
        return []

    def smart_global_crawler(self, max_iters_per_lang=3):
        print(f"[*] Starting Optimized Spider (20 Languages)...")
        extracted_titles = []
        
        for lang in self.languages:
            sources = self.multi_lang_sources.get(lang, [f"https://www.xvideos.com/?k={lang}"])
            initial_words = self.get_initial_keywords_from_home(random.choice(sources), lang)
            if not initial_words: initial_words = ["video", "clip"]
            
            current_active_queue = list(set(initial_words))
            iters = 0
            while current_active_queue and iters < max_iters_per_lang:
                keyword = current_active_queue.pop(0)
                if keyword in self.searched_history: continue
                self.searched_history.add(keyword)
                self.save_to_band_list(keyword)
                iters += 1
                
                safe_keyword = urllib.parse.quote(keyword)
                for base_url in sources:
                    search_url = f"{base_url}/search?q={safe_keyword}"
                    if "pornhub" in base_url: search_url = f"{base_url}video/search?search={safe_keyword}"
                    elif "xvideos" in base_url: search_url = f"{base_url}?k={safe_keyword}"
                    
                    try:
                        response = requests.get(search_url, headers=self.headers, timeout=5)
                        if response.status_code != 200: continue
                        soup = BeautifulSoup(response.text, 'html.parser')
                        titles = [el['title'].strip() for el in soup.find_all(['a', 'img', 'span'], title=True)]
                        for t in titles:
                            if 25 < len(t) < 160 and t not in extracted_titles:
                                extracted_titles.append(t)
                                if len(current_active_queue) < 20:
                                    current_active_queue.extend(self.dynamic_extract_keywords(t, lang))
                    except: continue
        self.phrases_global = list(set(extracted_titles))

    def update_all_existing_files_dates(self):
        print("[*] Syncing History for Google Freshness Filter...")
        base_time = datetime.now(timezone.utc)
        count = 0
        for root, dirs, files in os.walk("."):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        
                        new_time = base_time - timedelta(seconds=random.randint(0, 10800))
                        new_iso = new_time.strftime("%Y-%m-%dT%H:%M:%S+00:00")
                        new_sql = new_time.strftime("%Y-%m-%d %H:%M:%S")

                        content = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', new_iso, content)
                        content = re.sub(r'\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}', new_sql, content)
                        content = re.sub(r'("landingtime":\s*)\d+', rf'\1{random.randint(10, 30)}', content)

                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        count += 1
                    except: continue
        print(f"[*] Synced {count} files.")

    def run_single_cycle(self, count=500):
        self.update_all_existing_files_dates()
        
        if not self.phrases_global:
            self.phrases_global = ["Global Dynamic Video " + str(i) for i in range(100)]

        folder_main = ''.join(random.choices(string.ascii_lowercase, k=3))
        folder_sub = ''.join(random.choices(string.ascii_lowercase, k=3))
        target_dir = os.path.join(folder_main, folder_sub)
        os.makedirs(target_dir, exist_ok=True)
        
        all_pages = []
        base_time = datetime.now(timezone.utc)
        for i in range(count):
            raw_t = random.choice(self.phrases_global)
            final_title = f"{random.choice(self.emojis)} {raw_t} {random.choice(self.emojis)}"
            uid = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
            slug = re.sub(r'[^\w\u0600-\u06FF\u4e00-\u9fff\uac00-\ud7af\u0e00-\u0e7f\s-]', '', raw_t)
            slug = re.sub(r'\s+', '-', slug.strip().lower())[:70]
            fname = f"{slug}-{uid}.html"
            
            file_time = base_time - timedelta(seconds=random.randint(0, 3600))
            
            # التعديل الأساسي: اختيار قالب عشوائي من القائمة المتوفرة
            chosen_template = random.choice(self.template_names)
            
            all_pages.append({
                "title": final_title, "filename": fname, 
                "desc": ". ".join(random.sample(self.phrases_global, min(5, len(self.phrases_global)))), 
                "path": target_dir, 
                "template": chosen_template,
                "date_iso": file_time.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
                "date_sql": file_time.strftime("%Y-%m-%d %H:%M:%S")
            })

        for p in all_pages:
            content = self.templates.get(p['template'], "")
            related = random.sample(all_pages, min(len(all_pages), 12))
            links_html = "<div class='related-links'><ul>" + "".join([f"<li><a href='/{l['path']}/{l['filename']}'>{l['title']}</a></li>" for l in related]) + "</ul></div>"
            
            temp_content = content.replace("{{TITLE}}", p['title'])
            temp_content = temp_content.replace("{{DESCRIPTION}}", p['desc'])
            temp_content = temp_content.replace("{{INTERNAL_LINKS}}", links_html)
            temp_content = temp_content.replace("{{DATE}}", p['date_iso'])
            temp_content = temp_content.replace("{{DATE_SQL}}", p['date_sql'])
            
            temp_content = re.sub(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})', p['date_iso'], temp_content)
            
            with open(os.path.join(p['path'], p['filename']), "w", encoding="utf-8") as f:
                f.write(temp_content)
        
        print(f"✅ Deployment Complete: {count} pages generated using multiple templates.")

if __name__ == "__main__":
    generator = ContinuousGenerator()
    generator.run_single_cycle(count=500)

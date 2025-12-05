#!/usr/bin/env python3
import csv, sys, os, subprocess

def read_urls(path):
    urls=[]
    if path.lower().endswith('.csv'):
        with open(path,newline='',encoding='utf-8') as f:
            r=csv.DictReader(f)
            if 'url' in r.fieldnames:
                for row in r:
                    u=(row.get('url') or '').strip()
                    if u: urls.append(u)
            else:
                f.seek(0); r2=csv.reader(f)
                for row in r2:
                    if not row: continue
                    u=row[-1].strip()
                    if u.startswith('http'): urls.append(u)
    else:
        with open(path,encoding='utf-8') as f:
            for line in f:
                u=line.strip()
                if u.startswith('http'): urls.append(u)
    return urls

def main():
    if len(sys.argv)<3:
        print('Usage: python csv_to_mp3.py <csv_or_txt> <out_dir>')
        sys.exit(1)
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    urls = read_urls(src)
    if not urls:
        print('No URLs found.')
        sys.exit(2)
    print(f'Found {len(urls)} URLs. Downloading to {out} ...')
    for u in urls:
        subprocess.run(['yt-dlp','-x','--audio-format','mp3','-o',os.path.join(out,'%(title)s.%(ext)s'),u], check=False)
    print('Done.')

if __name__ == '__main__':
    main()

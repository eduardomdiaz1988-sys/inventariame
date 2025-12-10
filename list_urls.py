from django.urls import get_resolver

def list_urls():
    resolver = get_resolver()
    for pattern in resolver.url_patterns:
        print(pattern)

if __name__ == "__main__":
    list_urls()

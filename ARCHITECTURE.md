# Architektura PyTaskManager - Dokumentacja

## Struktura Projektu

```
PyTaskManager/
├── api/                          # Backend API (Flask)
│   ├── __init__.py
│   ├── app.py                    # Główna aplikacja Flask
│   ├── auth.py                   # Autentykacja JWT
│   ├── db.py                     # Konfiguracja bazy danych
│   └── models.py                 # Modele SQLAlchemy
│
├── desktop/                      # Frontend Desktop (Flet)
│   ├── components/               # ⭐ Komponenty wielokrotnego użytku
│   │   ├── admin_navbar.py       # Navbar dla admina + zakładki
│   │   ├── admin_task_manager.py # Zarządzanie taskami (admin)
│   │   ├── user_manager.py       # Zarządzanie użytkownikami (admin)
│   │   ├── user_navbar.py        # Navbar dla zwykłego użytkownika
│   │   ├── user_stats.py         # Statystyki tasków użytkownika
│   │   ├── user_task_manager.py  # Zarządzanie taskami (user)
│   │   └── task_card.py          # Karty pojedynczych tasków
│   │
│   ├── views/                    # 🖼️ Główne widoki aplikacji
│   │   ├── admin_view.py         # Panel administratora
│   │   ├── user_view.py          # Profil użytkownika
│   │   ├── tasks_view.py         # Lista tasków użytkownika
│   │   └── login_view.py         # Ekran logowania
│   │
│   ├── api_client.py             # Klient HTTP do API
│   ├── auth_manager.py           # Zarządzanie tokenami
│   ├── config.py                 # Konfiguracja aplikacji
│   └── main.py                   # Entry point aplikacji
│
├── create_admin.py               # Skrypt tworzenia admina
├── seed_data.py                  # Dane testowe
└── requirements.txt              # Zależności
```

## Architektura Komponentowa

### Zasada Separation of Concerns (SoC)

Projekt został zreorganizowany według zasady **pojedynczej odpowiedzialności**:

#### 1. **Views (Widoki)** - Logika wysokiego poziomu
- `admin_view.py` - Koordynuje widok admina, obsługuje przełączanie zakładek
- `user_view.py` - Wyświetla profil użytkownika
- `tasks_view.py` - Lista i zarządzanie taskami użytkownika
- `login_view.py` - Formularz logowania

#### 2. **Components (Komponenty)** - Elementy wielokrotnego użytku

##### Komponenty Admina:
- **`admin_navbar.py`**
  - `create_admin_navbar()` - Górna nawigacja dla admina
  - `create_admin_tabs()` - Zakładki przełączania Użytkownicy/Taski
  
- **`user_manager.py`**
  - Zarządzanie użytkownikami (CRUD)
  - Wyszukiwarka użytkowników
  - Dialog dodawania użytkowników z walidacją
  - Zwraca: `(widget, load_users_callback)`
  
- **`admin_task_manager.py`**
  - Zarządzanie taskami wszystkich użytkowników
  - Filtrowanie po użytkownikach
  - CRUD operacje na taskach
  - Zwraca: `(widget, load_tasks_callback)`

##### Komponenty Użytkownika:
- **`user_navbar.py`**
  - `create_user_navbar()` - Prosta nawigacja dla użytkownika
  
- **`user_stats.py`**
  - `create_user_stats()` - Widget statystyk (wszystkie/ukończone/do zrobienia)
  - Zwraca: `(widget, load_stats_callback)`
  
- **`user_task_manager.py`**
  - Zarządzanie własnymi taskami (CRUD)
  - Wyszukiwarka tasków
  - Dialogi dodawania i edycji z walidacją
  - Zwraca: `(widget, load_tasks_callback)`
  
- **`task_card.py`**
  - `create_task_card()` - Karta pojedynczego taska (użytkownik)
  - `create_admin_task_card()` - Karta taska z opcjami admina

## 🔄 Przepływ Danych

```
┌─────────────────────────────────────────────────────────────┐
│                       ADMIN VIEW                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ admin_navbar (Navbar + Logout)                       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ admin_tabs (Przełącznik: Użytkownicy / Taski)       │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Content Area (dynamiczny kontener)                   │  │
│  │  ┌────────────────┐  lub  ┌──────────────────────┐  │  │
│  │  │ user_manager   │       │ admin_task_manager   │  │  │
│  │  │ - Lista userów │       │ - Wszystkie taski    │  │  │
│  │  │ - Wyszukiwanie │       │ - Filtr po userze    │  │  │
│  │  │ - Dodawanie    │       │ - CRUD tasków        │  │  │
│  │  └────────────────┘       └──────────────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                       USER VIEW                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ user_navbar (Navbar + Logout)                        │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Avatar + Dane użytkownika                            │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ user_stats (Statystyki tasków)                       │  │
│  │ [Wszystkie] [Ukończone] [Do zrobienia]              │  │
│  └──────────────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ [Przycisk: Zarządzaj Taskami] → tasks_view          │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Zalety Nowej Architektury

### 1. **Modularność**
- Każdy komponent ma jedną, jasno określoną odpowiedzialność
- Łatwe testowanie poszczególnych komponentów
- Możliwość ponownego użycia komponentów

### 2. **Czytelność**
- `admin_view.py` zmniejszony z ~380 linii do ~85 linii
- `user_view.py` zmniejszony z ~140 linii do ~75 linii
- Logika podzielona na mniejsze, zrozumiałe części

### 3. **Łatwość Utrzymania**
- Zmiany w navbarze - jeden plik: `admin_navbar.py` lub `user_navbar.py`
- Zmiany w statystykach - jeden plik: `user_stats.py`
- Zmiany w zarządzaniu użytkownikami - jeden plik: `user_manager.py`

### 4. **Separacja Logiki**
- **Views** - koordynacja i routing
- **Components** - logika biznesowa i UI
- **API Client** - komunikacja z backendem

### 5. **Callback Pattern**
- Komponenty zwracają callbacki do ładowania danych
- Parent view kontroluje kiedy dane są ładowane
- Łatwa synchronizacja stanu

## 🔧 Wzorce Użyte

### 1. **Component Factory Pattern**
```python
# Komponenty zwracają tuple (widget, callback)
widget, load_callback = create_user_manager(page, api)
load_callback()  # Załaduj dane kiedy potrzeba
```

### 2. **Dependency Injection**
```python
# Komponenty otrzymują zależności jako parametry
def create_user_manager(page: ft.Page, api: APIClient):
    # ...
```

### 3. **Single Responsibility Principle**
- Każdy plik/funkcja ma jedną odpowiedzialność
- `admin_navbar.py` - tylko nawigacja admina
- `user_manager.py` - tylko zarządzanie użytkownikami

### 4. **Don't Repeat Yourself (DRY)**
- Wspólna logika w komponentach
- Wielokrotne użycie navbarów, statystyk, kart tasków

## 📝 Przykłady Użycia

### Admin View
```python
from components.admin_navbar import create_admin_navbar, create_admin_tabs
from components.user_manager import create_user_manager
from components.admin_task_manager import create_admin_task_manager

# Tworzenie komponentów
users_widget, load_users = create_user_manager(page, api)
tasks_widget, load_tasks = create_admin_task_manager(page, api)
navbar = create_admin_navbar(page, user, on_logout, switch_users, switch_tasks)

# Użycie
load_users()  # Załaduj użytkowników
load_tasks()  # Załaduj taski
```

### User View
```python
from components.user_navbar import create_user_navbar
from components.user_stats import create_user_stats

# Tworzenie komponentów
navbar = create_user_navbar(page, user, on_logout)
stats_widget, load_stats = create_user_stats(page, api)

# Użycie
load_stats()  # Załaduj statystyki
```

## 🚀 Możliwe Rozszerzenia

1. **Dodatkowe komponenty**:
   - `user_profile_card.py` - Karta profilu użytkownika
   - `task_filters.py` - Zaawansowane filtry tasków
   - `notification_center.py` - Centrum powiadomień

2. **Współdzielone komponenty**:
   - `common_dialogs.py` - Dialogi używane w całej aplikacji
   - `loading_spinner.py` - Wskaźnik ładowania
   - `error_display.py` - Wyświetlanie błędów

3. **State Management**:
   - Możliwość dodania globalnego state managera
   - Obsługa cache'owania danych

## 📊 Metryki Przed/Po

| Plik | Przed | Po | Redukcja |
|------|-------|-----|----------|
| `admin_view.py` | ~380 linii | ~85 linii | **77%** |
| `user_view.py` | ~140 linii | ~75 linii | **46%** |
| `tasks_view.py` | ~300 linii | ~80 linii | **73%** |
| **Komponenty** | 2 pliki | 8 plików | +6 (modularnych) |

## 🎯 Wnioski

Nowa architektura:
- ✅ Bardziej modularna i skalowalna
- ✅ Łatwiejsza w utrzymaniu
- ✅ Kod jest bardziej czytelny
- ✅ Komponenty są wielokrotnego użytku
- ✅ Łatwiejsze testowanie
- ✅ Zgodna z best practices

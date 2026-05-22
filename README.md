# ORHUN PROGRAMLAMA DİLİ

## Proje Hakkında

Orhun, Türk tarihi ve Orhun Yazıtları’ndan esinlenerek geliştirilmiş yorumlanan (interpreted) eğitim amaçlı bir programlama dilidir.

Bu proje:
- Lexer
- Parser
- AST (Abstract Syntax Tree)
- Semantic Analysis
- Interpreter

bileşenlerinden oluşmaktadır.

Dil Python kullanılarak geliştirilmiştir.

---

# Dil Özellikleri

- Özgün Türk tarihi temalı syntax
- Custom keyword sistemi
- Değişken tanımlama
- Matematiksel işlemler
- Metin işlemleri
- Boolean işlemleri
- if-else yapısı
- while döngüsü
- kurultay (switch-case benzeri yapı)
- Syntax Error sistemi
- Semantic Error sistemi
- AST üretimi

---

# Anahtar Kelimeler

| Yapı | Keyword |
|---|---|
| program başlangıcı | `bitig` |
| değişken tanımlama | `tamga` |
| integer | `sayi` |
| string | `yazi` |
| boolean | `kut` |
| true | `var` |
| false | `yok` |
| print | `sesver` |
| if | `yokla` |
| else | `yada` |
| while | `yuru` |
| switch | `kurultay` |
| case | `boy` |
| default | `son` |

---

# Orhun Interpreter Pipeline

```text
Source Code (.orh)
        ↓
Lexer
        ↓
Token Stream
        ↓
Parser
        ↓
Abstract Syntax Tree (AST)
        ↓
Semantic Analysis
        ↓
Interpreter
        ↓
Program Output
```

---

# Proje Yapısı

```text
Orhun/
│
├── src/
│   ├── main.py
│   ├── lexer.py
│   ├── parser.py
│   ├── ast_nodes.py
│   ├── interpreter.py
│   ├── semantic.py
│   ├── tokens.py
│   └── errors.py
│
├── examples/
│   ├── ordu.orh
│   ├── dongu.orh
│   ├── kurultay.orh
│   └── hata.orh
│
├── README.md
├── ai_prompts.md
└── requirements.txt
```

---

# Kurulum

## Python Kurulumu

Python 3.10+ önerilir.

Python sürümünü kontrol etmek için:

```bash
python --version
```

---

# Çalıştırma

## Örnek Program Çalıştırma

```bash
python src/main.py examples/ordu.orh
```

---

# Örnek Orhun Programı

```orhun
bitig {

    tamga sayi asker = 100;
    tamga yazi lider = "Bilge Kagan";

    sesver("Ordu Hazir");
    sesver(lider);

    yokla (asker > 50) {

        sesver("Ordu guclu");

    } yada {

        sesver("Takviye gerekli");
    }
}
```

---

# Örnek Çıktı

```text
Ordu Hazir
Bilge Kagan
Ordu guclu
```

---

# Lexer

Lexer:
- kaynak kodu karakter karakter okur
- token üretir
- parser modülüne aktarır

Örnek token çıktısı:

```text
Token(KEYWORD, bitig)
Token(KEYWORD, tamga)
Token(KEYWORD, sayi)
Token(IDENTIFIER, asker)
Token(NUMBER, 100)
```

---

# Parser

Parser:
- tokenları analiz eder
- syntax kontrolü yapar
- AST üretir

Örnek AST:

```text
VarDeclNode
├── type: sayi
├── name: asker
└── value:
    NumberNode(100)
```

---

# Semantic Analysis

Semantic analyzer:
- tip kontrolü yapar
- tanımlanmamış değişkenleri kontrol eder

Örnek semantic hata:

```text
Semantic Error:
sayi tipine uygun olmayan değer.
```

---

# Syntax Error Sistemi

Örnek syntax hatası:

```text
Parser Error:
Geçersiz ifade.
```

---

# Kullanılan Teknolojiler

- Python
- Recursive Descent Parser
- AST (Abstract Syntax Tree)
- Interpreter Pattern

---

# Geliştirici

KARDELEN YENİEKİNCİ

BIL206 - Programlama Dillerinin Prensipleri
Dönem Ödevi
from vpython import *
import random

# Pengaturan scene
scene = canvas(width=800, height=600)

# Membuat dinding kotak
a = 7
dinding_kanan = box(pos=vector(a, 0, 0), size=vector(0.1, 2*a, 2*a), color=color.white)
dinding_kiri = box(pos=vector(-a, 0, 0), size=vector(0.1, 2*a, 2*a), color=color.white)
dinding_atas = box(pos=vector(0, a, 0), size=vector(2*a, 0.1, 2*a), color=color.white)
dinding_bawah = box(pos=vector(0, -a, 0), size=vector(2*a, 0.1, 2*a), color=color.white)
dinding_belakang = box(pos=vector(0, 0, -a), size=vector(2*a, 2*a, 0.1), color=color.white)

# Fungsi untuk menghasilkan posisi acak tanpa tumpang tindih
def posisi_acak(posisi_eksisting, jari_jari):
    while True:
        pos = vector(random.uniform(-a+1, a-1), random.uniform(-a+1, a-1), 0)
        if all(mag(pos - p) > 2*jari_jari for p in posisi_eksisting):
            return pos

# Membuat bola dengan warna berbeda
warna_bola = [color.red, color.green, color.cyan, color.black, color.orange]
bola_bola = []
jari_jari_bola = 0.6
posisi_bola = []

for warna in warna_bola:
    pos = posisi_acak(posisi_bola, jari_jari_bola)
    posisi_bola.append(pos)
    bola_bola.append(sphere(pos=pos,
                            radius=jari_jari_bola, color=warna,
                            velocity=vector(random.uniform(-1, 1), random.uniform(-1, 1), 0),
                            stopped=False))

# Membuat bola ungu
bola_ungu = sphere(pos=vector(0, 0, 0), radius=jari_jari_bola, color=color.purple, velocity=vector(0, 0, 0))

# Teks untuk jumlah tabrakan
jumlah_tabrakan = 0
teks_tabrakan = label(pos=vector(0, a+1, 0), text='Tabrakan: 0', color=color.yellow, height=20, box=False, opacity=0)

# Mode kontrol
mode_pantul = True

# Fungsi untuk mengubah mode
def ubah_mode():
    global mode_pantul
    mode_pantul = not mode_pantul
    tombol_mode.text = 'Mode: Pantul' if mode_pantul else 'Mode: Berhenti'

# Tombol mode
tombol_mode = button(text='Mode: Pantul', bind=ubah_mode, pos=scene.title_anchor)

# Fungsi kontrol keyboard untuk bola ungu
def gerak_bola_ungu(evt):
    s = evt.key
    if s in ['left']:
        bola_ungu.velocity.x = -1
    elif s in ['right']:
        bola_ungu.velocity.x = 1
    elif s in ['up']:
        bola_ungu.velocity.y = 1
    elif s in ['down']:
        bola_ungu.velocity.y = -1

scene.bind('keydown', gerak_bola_ungu)

# Fungsi untuk memperbarui posisi
def perbarui_posisi():
    global jumlah_tabrakan

    # Memperbarui posisi bola
    for bola in bola_bola:
        bola.pos += bola.velocity * dt

        # Cek tabrakan dengan dinding
        if bola.pos.x > a - jari_jari_bola or bola.pos.x < -a + jari_jari_bola:
            bola.velocity.x *= -1
        if bola.pos.y > a - jari_jari_bola or bola.pos.y < -a + jari_jari_bola:
            bola.velocity.y *= -1

        # Cek tabrakan dengan bola lain
        for bola_lain in bola_bola:
            if bola != bola_lain and mag(bola.pos - bola_lain.pos) < 2 * jari_jari_bola:
                bola.velocity, bola_lain.velocity = bola_lain.velocity, bola.velocity

        # Cek tabrakan dengan bola ungu
        if mag(bola.pos - bola_ungu.pos) < 2 * jari_jari_bola:
            if mode_pantul:
                bola.velocity, bola_ungu.velocity = bola_ungu.velocity, bola.velocity
            else:
                bola.velocity = vector(0, 0, 0)
            jumlah_tabrakan += 1
            teks_tabrakan.text = f'Tabrakan: {jumlah_tabrakan}'

    # Memperbarui posisi bola ungu
    bola_ungu.pos += bola_ungu.velocity * dt

    # Cek tabrakan dengan dinding untuk bola ungu
    if bola_ungu.pos.x > a - jari_jari_bola or bola_ungu.pos.x < -a + jari_jari_bola:
        bola_ungu.velocity.x *= -1
    if bola_ungu.pos.y > a - jari_jari_bola or bola_ungu.pos.y < -a + jari_jari_bola:
        bola_ungu.velocity.y *= -1

# Langkah waktu
dt = 0.01

# Loop utama
while True:
    rate(100)
    perbarui_posisi()

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

# encode.py と decode.py から関数をインポート
from encode import encode_firmata_stream
from decode import decode_firmata

def gui_encode():
    input_text = encode_input.get("1.0", tk.END).strip()
    try:
        # 入力は、スペース区切りの16進数文字列 (例: "10 20 30 40 ...")
        data = [int(x, 16) for x in input_text.split()]
        encoded = encode_firmata_stream(data)
        output = " ".join("{:02X}".format(b) for b in encoded)
        encode_output.delete("1.0", tk.END)
        encode_output.insert(tk.END, output)
    except Exception as e:
        encode_output.delete("1.0", tk.END)
        encode_output.insert(tk.END, "Error: " + str(e))

def gui_decode():
    input_text = decode_input.get("1.0", tk.END).strip()
    try:
        data = [int(x, 16) for x in input_text.split()]
        decoded = decode_firmata(data)
        output = " ".join("{:02X}".format(b) for b in decoded)
        decode_output.delete("1.0", tk.END)
        decode_output.insert(tk.END, output)
    except Exception as e:
        decode_output.delete("1.0", tk.END)
        decode_output.insert(tk.END, "Error: " + str(e))

# メインウィンドウの作成
root = tk.Tk()
root.title("Firmata Encoder/Decoder")
root.geometry("800x600")  # 初期サイズを大きく設定

# エンコード用のフレーム
encode_frame = ttk.LabelFrame(root, text="エンコード")
encode_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

ttk.Label(encode_frame, text="エンコード対象の8ビットデータ (例: 10 20 30 40 50 60 70 80 90 A0 B0 C0)").pack(anchor="w", padx=5, pady=5)
encode_input = scrolledtext.ScrolledText(encode_frame, width=80, height=5)
encode_input.pack(padx=5, pady=5)
ttk.Button(encode_frame, text="エンコード", command=gui_encode).pack(pady=5)
ttk.Label(encode_frame, text="エンコード結果 (7ビットパック済み) MIDIやFirmata上の値").pack(anchor="w", padx=5, pady=5)
encode_output = scrolledtext.ScrolledText(encode_frame, width=80, height=5)
encode_output.pack(padx=5, pady=5)

# デコード用のフレーム
decode_frame = ttk.LabelFrame(root, text="デコード")
decode_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

ttk.Label(decode_frame, text="デコード対象の7ビットパック済みデータ (例: 10 40 40 01 04 0A 18 38 00 21 02 05 0B 18) MIDIやFirmata上の値").pack(anchor="w", padx=5, pady=5)
decode_input = scrolledtext.ScrolledText(decode_frame, width=80, height=5)
decode_input.pack(padx=5, pady=5)
ttk.Button(decode_frame, text="デコード", command=gui_decode).pack(pady=5)
ttk.Label(decode_frame, text="デコード結果 (元の8ビットデータ)").pack(anchor="w", padx=5, pady=5)
decode_output = scrolledtext.ScrolledText(decode_frame, width=80, height=5)
decode_output.pack(padx=5, pady=5)

root.mainloop()

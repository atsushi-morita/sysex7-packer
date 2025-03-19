def decode_firmata(encoded):
    """
    encoded: 7ビットにパックされた整数のリスト（各値は 0～127 の範囲）
    戻り値: 復元された8ビットデータのリスト
    """
    bit_buffer = 0
    bit_count = 0
    decoded = []
    for b in encoded:
        # 7ビット分をビットバッファに追加
        bit_buffer |= (b << bit_count)
        bit_count += 7
        # バッファに8ビット以上溜まっていれば、下位8ビットを取り出す
        while bit_count >= 8:
            decoded_byte = bit_buffer & 0xFF
            decoded.append(decoded_byte)
            bit_buffer >>= 8
            bit_count -= 8
    return decoded

def main():
    #SysExのエンコードされたデータ部（16進表現）
    hex_data = "10 40 40 01 04 0A 18 38 00 21 02 05 0B 18 56 53 21 68 00"


    encoded_bytes = [int(x, 16) for x in hex_data.split()]
    
    decoded = decode_firmata(encoded_bytes)
    
    print("元データ ({} バイト):".format(len(hex_data)))
    print(hex_data)

    print("\n復元された全データ ({} バイト):".format(len(decoded)))
    print(" ".join("{:02X}".format(b) for b in decoded))
    
if __name__ == "__main__":
    main()
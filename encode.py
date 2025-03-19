def encode_firmata_stream(data, max_bytes=None):
    """
    Firmataの encodeByteStream() を再現するエンコーダー
    data: 元のバイト列（整数のリスト、各値0～255）
    max_bytes: 送信する最大バイト数。Noneの場合は制限なし
    戻り値: エンコード後のバイト列（各値は下位7ビットに意味がある）
    """
    transmit_bits = 7
    transmit_mask = (1 << transmit_bits) - 1  # 0x7F
    if max_bytes is None:
        max_bytes = float('inf')
    
    encoded = []
    bytes_sent = 0
    outstanding_bits = 0
    # 初期状態：先頭の元データの値をキャッシュに設定
    outstanding_bit_cache = data[0]
    
    bytec = len(data)
    for i in range(bytec):
        if bytes_sent >= max_bytes:
            break
        
        # 送信バイト = outstanding_bit_cache OR (data[i] << outstanding_bits)
        transmit_byte = (outstanding_bit_cache | ((data[i] << outstanding_bits) & 0xFF)) & 0xFF
        encoded.append(transmit_byte & transmit_mask)
        bytes_sent += 1
        
        # outstanding_bit_cache を更新
        shift_val = transmit_bits - outstanding_bits  # (7 - outstanding_bits)
        outstanding_bit_cache = (data[i] >> shift_val) & 0xFF
        outstanding_bits += (8 - transmit_bits)  # この例では常に +1（8-7）
        
        # outstanding_bits が transmit_bits (7) 以上なら、残ったビットを送信する
        while outstanding_bits >= transmit_bits and bytes_sent < max_bytes:
            transmit_byte = outstanding_bit_cache & 0xFF
            encoded.append(transmit_byte & transmit_mask)
            bytes_sent += 1
            outstanding_bit_cache = (outstanding_bit_cache >> transmit_bits) & 0xFF
            outstanding_bits -= transmit_bits

    # 余ったビットがあればフラッシュ（不足分の1ビット未満は無視）
    if outstanding_bits and bytes_sent < max_bytes:
        final_byte = ((1 << outstanding_bits) - 1) & outstanding_bit_cache
        encoded.append(final_byte)
        bytes_sent += 1

    return encoded

def main():
    # 元のデータ
    orig_hex = "10 20 30 40 50 60 70 80 90 A0 B0 C0 58 A7 21 34"
    data = [int(x, 16) for x in orig_hex.split()]
    
    encoded = encode_firmata_stream(data)
    
    # エンコード結果を16進数文字列に変換
    encoded_hex = " ".join("{:02X}".format(b) for b in encoded)
    print("元データ ({} バイト):".format(len(data)))
    print(orig_hex)
    print("\nエンコード結果: ({} バイト):".format(len(encoded_hex)))
    print(encoded_hex)
    
if __name__ == "__main__":
    main()
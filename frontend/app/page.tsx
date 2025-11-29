'use client'

import axios from 'axios';
import { useCallback, useEffect, useState } from 'react';
import { QRCodeSVG } from 'qrcode.react';
import Barcode from 'react-barcode';
import styles from './page.module.css';

interface CodeData {
  id: number;
  text: string;
  code_type: 'qr_code' | 'barcode';
  qr_format: string;
  barcode_format: string;
  created_at: string;
  updated_at: string;
}

interface Choice {
  value: string;
  label: string;
}

interface Choices {
  code_types: Choice[];
  qr_formats: Choice[];
  barcode_formats: Choice[];
}

export default function Page() {
  const [codes, setCodes] = useState<CodeData[]>([]);
  const [choices, setChoices] = useState<Choices | null>(null);
  const [text, setText] = useState('');
  const [codeType, setCodeType] = useState<'qr_code' | 'barcode'>('qr_code');
  const [qrFormat, setQrFormat] = useState('qr_code');
  const [barcodeFormat, setBarcodeFormat] = useState('code128');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const apiUrl = process.env.NEXT_PUBLIC_API_URL;

  const fetchCodes = useCallback(async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/codes`);
      setCodes(response.data);
    } catch (err) {
      console.error('Failed to fetch codes:', err);
    }
  }, [apiUrl]);

  const fetchChoices = useCallback(async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/choices`);
      setChoices(response.data);
    } catch (err) {
      console.error('Failed to fetch choices:', err);
    }
  }, [apiUrl]);

  useEffect(() => {
    fetchCodes();
    fetchChoices();
  }, [fetchCodes, fetchChoices]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!text.trim()) {
      setError('テキストを入力してください');
      return;
    }
    setLoading(true);
    setError(null);
    try {
      await axios.post(`${apiUrl}/api/codes`, {
        text,
        code_type: codeType,
        qr_format: qrFormat,
        barcode_format: barcodeFormat,
      });
      setText('');
      fetchCodes();
    } catch (err) {
      setError('コードの作成に失敗しました');
      console.error('Failed to create code:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await axios.delete(`${apiUrl}/api/codes/${id}`);
      fetchCodes();
    } catch (err) {
      console.error('Failed to delete code:', err);
    }
  };

  type BarcodeFormatType = 'CODE39' | 'CODE128' | 'EAN13' | 'EAN8' | 'UPC' | 'ITF14' | 'CODE128A' | 'CODE128B' | 'CODE128C' | 'EAN5' | 'EAN2' | 'UPCE' | 'ITF' | 'MSI' | 'MSI10' | 'MSI11' | 'MSI1010' | 'MSI1110' | 'pharmacode' | 'codabar' | 'GenericBarcode';

  const getBarcodeFormatForLibrary = (format: string): BarcodeFormatType => {
    const formatMap: Record<string, BarcodeFormatType> = {
      code39: 'CODE39',
      code128: 'CODE128',
      ean13: 'EAN13',
      ean8: 'EAN8',
      upca: 'UPC',
      upce: 'UPCE',
      itf: 'ITF14',
    };
    return formatMap[format] || 'CODE128';
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>QRコード / バーコード ジェネレーター</h1>

      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.formGroup}>
          <label htmlFor="text">テキスト</label>
          <textarea
            id="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="QRコード/バーコードにしたいテキストを入力"
            rows={3}
            className={styles.textarea}
          />
        </div>

        <div className={styles.formGroup}>
          <label htmlFor="codeType">コードの種類</label>
          <select
            id="codeType"
            value={codeType}
            onChange={(e) => setCodeType(e.target.value as 'qr_code' | 'barcode')}
            className={styles.select}
          >
            {choices?.code_types.map((choice) => (
              <option key={choice.value} value={choice.value}>
                {choice.label}
              </option>
            ))}
          </select>
        </div>

        {codeType === 'qr_code' && (
          <div className={styles.formGroup}>
            <label htmlFor="qrFormat">QRコード規格</label>
            <select
              id="qrFormat"
              value={qrFormat}
              onChange={(e) => setQrFormat(e.target.value)}
              className={styles.select}
            >
              {choices?.qr_formats.map((choice) => (
                <option key={choice.value} value={choice.value}>
                  {choice.label}
                </option>
              ))}
            </select>
          </div>
        )}

        {codeType === 'barcode' && (
          <div className={styles.formGroup}>
            <label htmlFor="barcodeFormat">バーコード規格</label>
            <select
              id="barcodeFormat"
              value={barcodeFormat}
              onChange={(e) => setBarcodeFormat(e.target.value)}
              className={styles.select}
            >
              {choices?.barcode_formats.map((choice) => (
                <option key={choice.value} value={choice.value}>
                  {choice.label}
                </option>
              ))}
            </select>
          </div>
        )}

        {error && <p className={styles.error}>{error}</p>}

        <button type="submit" disabled={loading} className={styles.button}>
          {loading ? '作成中...' : 'コードを作成'}
        </button>
      </form>

      <h2 className={styles.subtitle}>作成済みコード一覧</h2>

      {codes.length === 0 ? (
        <p className={styles.empty}>まだコードがありません</p>
      ) : (
        <div className={styles.codeList}>
          {codes.map((code) => (
            <div key={code.id} className={styles.codeCard}>
              <div className={styles.codeDisplay}>
                {code.code_type === 'qr_code' ? (
                  <QRCodeSVG value={code.text} size={150} />
                ) : (
                  <Barcode
                    value={code.text}
                    format={getBarcodeFormatForLibrary(code.barcode_format)}
                    width={1.5}
                    height={60}
                    fontSize={12}
                  />
                )}
              </div>
              <div className={styles.codeInfo}>
                <p className={styles.codeText}>{code.text}</p>
                <p className={styles.codeType}>
                  種類: {code.code_type === 'qr_code' ? 'QRコード' : 'バーコード'}
                </p>
                <p className={styles.codeFormat}>
                  規格: {code.code_type === 'qr_code' ? code.qr_format : code.barcode_format}
                </p>
                <button
                  onClick={() => handleDelete(code.id)}
                  className={styles.deleteButton}
                >
                  削除
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

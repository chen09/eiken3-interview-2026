import { CaretDown, Translate } from '@phosphor-icons/react';

export type TranslationLanguage = 'ja' | 'zh';
export type BilingualText = Record<TranslationLanguage, string>;

type TranslationProps = {
  value: BilingualText;
  title?: BilingualText;
  tip?: BilingualText;
  alternatives?: BilingualText[];
  label: string;
  language: TranslationLanguage;
  onLanguageChange: (language: TranslationLanguage) => void;
};

export function Translation({
  value,
  title,
  tip,
  alternatives = [],
  label,
  language,
  onLanguageChange,
}: TranslationProps) {
  return (
    <details className="translation">
      <summary aria-label={`${label}の訳を見る`}>
        <Translate size={17} aria-hidden="true" />
        <span>訳を見る</span>
        <span className="translation-hint">日本語 / 中文</span>
        <CaretDown className="translation-caret" size={14} aria-hidden="true" />
      </summary>
      <div className="translation-body">
        <div className="translation-switch" role="group" aria-label="訳文の言語">
          <button
            type="button"
            aria-pressed={language === 'ja'}
            onClick={() => onLanguageChange('ja')}
          >
            日本語
          </button>
          <button
            type="button"
            aria-pressed={language === 'zh'}
            onClick={() => onLanguageChange('zh')}
          >
            中文
          </button>
        </div>
        <div className="translation-copy" lang={language === 'zh' ? 'zh-CN' : 'ja'}>
          {title && <strong>{title[language]}</strong>}
          <p>{value[language]}</p>
          {tip && <div className="translation-tip">
            <span>{language === 'ja' ? 'ヒント' : '提示'}</span>
            <p>{tip[language]}</p>
          </div>}
          {alternatives.length > 0 && (
            <div className="translation-alternatives">
              <span>{language === 'ja' ? 'ほかの例' : '其他示例'}</span>
              {alternatives.map((alternative, index) => (
                <p key={index}>{alternative[language]}</p>
              ))}
            </div>
          )}
        </div>
      </div>
    </details>
  );
}

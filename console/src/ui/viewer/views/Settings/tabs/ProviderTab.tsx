import React, { useState } from 'react';
import { Card, CardBody, CardTitle, Input, Button, Icon } from '../../../components/ui';

interface ProviderTabProps {
  settings: Record<string, any>;
  onSettingChange: (key: string, value: any) => void;
}

interface ApiKeyInputProps {
  label: string;
  placeholder?: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}

function ApiKeyInput({ label, placeholder, value, onChange }: ApiKeyInputProps) {
  const [showKey, setShowKey] = useState(false);

  return (
    <div className="form-control w-full">
      <label className="label">
        <span className="label-text">{label}</span>
      </label>
      <div className="flex gap-2">
        <input
          type={showKey ? 'text' : 'password'}
          placeholder={placeholder}
          value={value}
          onChange={onChange}
          className="input input-bordered w-full flex-1"
        />
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setShowKey(!showKey)}
          className="btn-square"
        >
          <Icon icon={showKey ? 'lucide:eye-off' : 'lucide:eye'} size={18} />
        </Button>
      </div>
      {value && (
        <label className="label">
          <span className="label-text-alt text-success">Key configured ({value.length} chars)</span>
        </label>
      )}
    </div>
  );
}

export function ProviderTab({ settings, onSettingChange }: ProviderTabProps) {
  return (
    <div className="space-y-6">
      <Card>
        <CardBody>
          <CardTitle>Claude (Anthropic)</CardTitle>
          <p className="text-sm text-base-content/60 mb-4">
            Configure the Claude API for memory compression
          </p>
          <div className="space-y-4">
            <ApiKeyInput
              label="API Key (optional - uses environment variable if not set)"
              placeholder="sk-ant-..."
              value={settings.CLAUDE_PILOT_ANTHROPIC_API_KEY || ''}
              onChange={(e) => onSettingChange('CLAUDE_PILOT_ANTHROPIC_API_KEY', e.target.value)}
            />
            <Input
              label="Model"
              placeholder="claude-sonnet-4-20250514"
              value={settings.CLAUDE_PILOT_MODEL || 'claude-sonnet-4-20250514'}
              onChange={(e) => onSettingChange('CLAUDE_PILOT_MODEL', e.target.value)}
            />
          </div>
        </CardBody>
      </Card>
    </div>
  );
}

import React from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogTrigger,
} from '../components/ui/dialog';
import { Button } from '../components/ui/button';

interface TxDetailModalProps {
  triggerLabel?: string;
  title: string;
  from: string;
  to: string;
  amount: string;
  date?: string;
}

const TxDetailModal: React.FC<TxDetailModalProps> = ({
  triggerLabel = 'View Details',
  title,
  from,
  to,
  amount,
  date,
}) => {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <div className="cursor-pointer hover:text-indigo-300 transition">{triggerLabel}</div>
      </DialogTrigger>

      <DialogContent className="bg-gray-900 text-white border-gray-700">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription className="text-gray-400 text-sm">
            Here are the details of this transaction.
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-2 text-sm mt-4">
          <p>
            <strong>From:</strong> {from}
          </p>
          <p>
            <strong>To:</strong> {to}
          </p>
          <p>
            <strong>Amount:</strong> {amount} NTR
          </p>
          {date && (
            <p>
              <strong>Date:</strong> {date}
            </p>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default TxDetailModal;

import Image from 'next/image'
import parse from 'html-react-parser';
import { useToast } from '@/components/ui/use-toast';
import { Suspense, useEffect, useState } from 'react';
import DisplayComponent from './DisplayComponent';
import dynamic from 'next/dynamic';
import UserInput from './UserInput';


export default function Home() {


  return (
    <div className="mx-auto max-w-5xl mt-40">
      <UserInput />
    </div>
  )
}

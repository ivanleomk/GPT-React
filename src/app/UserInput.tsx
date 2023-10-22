"use client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { useToast } from "@/components/ui/use-toast";
import { ClearComponent, SubmitPrompt } from "@/lib/prompt";
import dynamic from "next/dynamic";
import React, { useState, useTransition } from "react";
import { ClipLoader } from "react-spinners";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const DynamicHeader = dynamic(() => import("../generated/component"), {
  loading: () => <p>Loading...</p>,
  ssr: false, // add this line to disable server-side rendering
});

const UserInput = () => {
  const [isPending, startTransition] = useTransition();
  const [userInput, setuserInput] = useState("");
  const [generatedCode, setGeneratedCode] = useState("");

  return (
    <div className="max-w-xl mx-auto">
      <h1>GPT-4 Powered React Components</h1>

      <form
        className="my-4 "
        onSubmit={(e) => {
          e.preventDefault();
          startTransition(() => {
            SubmitPrompt(userInput).then((res) => {
              setGeneratedCode(res["code"]);
            });
          });
        }}
      >
        <Label>Prompt</Label>
        <Textarea
          value={userInput}
          onChange={(e) => setuserInput(e.target.value)}
          placeholder="I want to create a login form that..."
        />
        <div className="flex items-center justify-end mt-6 space-x-4">
          <Button type="submit">Submit</Button>
        </div>
      </form>

      {isPending ? (
        <>
          {" "}
          <ClipLoader speedMultiplier={0.4} size={30} />{" "}
          <span>Generating Component...</span>
        </>
      ) : generatedCode.length === 0 ? (
        <p className="text-center">No Component Generated yet</p>
      ) : (
        <Tabs defaultValue="code">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="code">Code</TabsTrigger>
            <TabsTrigger value="component">Component</TabsTrigger>
          </TabsList>
          <TabsContent value="code">
            <code className="relative rounded px-[0.3rem] py-[0.2rem] font-mono text-sm">
              {generatedCode.split("\n").map((item) => (
                <div className="py-1 px-4 bg-muted">{item}</div>
              ))}
            </code>
          </TabsContent>
          <TabsContent value="component">
            <div className="mt-6 border px-6 py-6">
              <DynamicHeader />
            </div>
          </TabsContent>
        </Tabs>
      )}
    </div>
  );
};

export default UserInput;

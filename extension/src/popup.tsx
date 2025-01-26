import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { X, Hash, Check } from "lucide-react";
import { Card, CardContent } from "./components/ui/card";
import { ScrollArea } from "./components/ui/scroll-area";
import "./globals.css";

interface APIData {
  url: string;
  summary: string;
  relatedArticles: {
    url: string;
    title: string;
  }[];
  status: "good" | "bad" | "unreliable";
  trustLevel: number;
}

interface Metric {
  label: string;
  value: number;
}

const Popup = () => {
  const [data, setData] = useState<APIData | null>(null);
  const [currentURL, setCurrentURL] = useState<string>("");
  const [expandedSummary, setExpandedSummary] = useState(false);
  const [expandedTrust, setExpandedTrust] = useState(false);

  console.log("frontend Data:", data);

  useEffect(() => {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      if (tabs[0]?.url) {
        setCurrentURL(tabs[0].url);
      }
    });

    chrome.runtime.sendMessage({ type: "GET_DATA" }, (response) => {
      console.log("Received response:", response);
      if (chrome.runtime.lastError) {
        console.error("Error:", chrome.runtime.lastError);
        return;
      }
      setData(response);
    });
  }, []);

  if (!data) return <div className="p-4">Loading data...</div>;

  const statusText =
    data.status === "good"
      ? "Trustworthy"
      : data.status === "bad"
      ? "Untrustworthy"
      : "Unreliable";
  // const statusColor = data.status === "good" ? "text-green-500" : data.status === "bad" ? "text-red-500" : "text-yellow-500";
  const statusImage =
    data.status === "good"
      ? "/good.png"
      : data.status === "bad"
      ? "/bad.png"
      : "/unreliable.png";

  const metrics: Metric[] = [
    {
      label: "Information Accuracy",
      value: 98,
    },
    {
      label: "Source Credibility",
      value: 85,
    },
    {
      label: "Public Interest",
      value: 70,
    },
    {
      label: "Headline Integrity",
      value: 90,
    },
  ];

  return (
    <div className="w-[300px] bg-zinc-900 text-white font-sans p-[6px] pb-[14px] space-y-4 relative">
      {/* Header */}
      <div className="flex justify-between items-center p-2">
        <img src="/logo.png" className="w-fit h-[30px]" />
      </div>

      {/* Trust Indicator */}
      <Card className="bg-zinc-800/50 border-zinc-700 mx-2">
        <CardContent className="p-0">
          <div className="flex items-center gap-1 max-h-[90px] overflow-hidden">
            <img
              src={statusImage}
              className="w-[100px] h-[100px] object-cover"
            />
            <div className="mr-2">
              <div className="text-zinc-400 text-[12px]">
                {new URL(currentURL).hostname}
              </div>

              <div
                className={`text-[22px] leading-[24px] font-semibold text-white`}
              >
                {statusText}
              </div>
              {/* <button
                onClick={() => setExpandedTrust(!expandedTrust)}
                className="text-zinc-400 hover:text-zinc-300 text-[12px] underline"
              >
                {expandedTrust ? "Minimize" : "Why?"}
              </button> */}
            </div>
          </div>
          {expandedTrust && (
            <div className="p-3 space-y-2">
              {metrics.map((metric, index) => (
                <div key={index} className="space-y-1">
                  <div className="flex items-center justify-between text-[12px]">
                    <span className="text-zinc-400">{metric.label}</span>
                    <span className="text-zinc-300">{metric.value}%</span>
                  </div>
                  <div className="h-1.5 w-full bg-zinc-700/50 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-emerald-500 to-emerald-400/80 transition-all duration-500"
                      style={{ width: `${metric.value}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Summary */}
      <Card
        className="mx-2 mb-2 bg-zinc-800/50 border-zinc-700 cursor-pointer"
        onClick={() => setExpandedSummary(!expandedSummary)}
      >
        <CardContent className="p-3">
          <h2 className="text-[14px] font-medium mb-2 text-white">Summary</h2>
          <p className="text-zinc-400 leading-relaxed text-[12px]">
            {expandedSummary
              ? data.summary
              : `${data.summary.substring(0, 150)}...`}
          </p>
        </CardContent>
      </Card>

      {/* Related Articles */}
      {data.relatedArticles.length > 0 && (
        <Card className="mx-2 bg-zinc-800/50 border-zinc-700">
          <CardContent className="p-3">
            <h2 className="text-[14px] font-medium mb-2 text-white">
              Related Articles
            </h2>
            <ScrollArea className="w-[250px] whitespace-nowrap overflow-scroll">
              <div className="flex w-max space-x-2">
                {data.relatedArticles.map((article, i) => (
                  <a href={article.url} target="_blank" key={i}>
                    <Card className="bg-[#1C1C1E] border-[#323136] w-[94px] flex-shrink-0 rounded-[2px]">
                      <CardContent className="p-1">
                        <div className="space-y-2">
                          <div className="text-[8px] text-white whitespace-normal">
                            {article.title.substring(0, 50)}
                          </div>
                          <div className="flex items-center gap-1.5 text-xs text-zinc-400">
                            <span className="text-[8px]">
                              {new URL(article.url).hostname}
                            </span>
                          </div>
                        </div>
                      </CardContent>
                    </Card>
                  </a>
                ))}
              </div>
            </ScrollArea>
          </CardContent>
        </Card>
      )}

      {expandedSummary && (
        <div className="absolute inset-0 z-20 bg-zinc-900/80 flex items-center justify-center p-3 !m-0">
          <Card className="w-full h-full bg-zinc-800/90 border-zinc-700 overflow-auto">
            <CardContent className="p-4">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-[14px] font-medium text-white">
                  Full Summary
                </h2>
                <button
                  onClick={() => setExpandedSummary(false)}
                  className="text-zinc-400 hover:text-white"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>
              <p className="text-zinc-400 leading-relaxed">{data.summary}</p>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};

const root = createRoot(document.getElementById("root")!);
root.render(
  <React.StrictMode>
    <Popup />
  </React.StrictMode>
);

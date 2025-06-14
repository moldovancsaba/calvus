import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import Game from "./pages/Game";
import DocumentsPage from "./pages/Documents";
import SettingsPage from "./pages/Settings";
import IdentityProvider from "./components/IdentityContext";
import IdentityGate from "./components/IdentityGate";

const queryClient = new QueryClient();

const App = () => (
  <IdentityProvider>
    <IdentityGate>
      <QueryClientProvider client={queryClient}>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<Index />} />
              <Route path="/game">
                <Route index element={<Game />} />
                <Route path=":slug" element={<Game />} />
              </Route>
              <Route path="/settings" element={<SettingsPage />} />
              <Route path="/documents" element={<DocumentsPage />} />
              <Route path="*" element={<NotFound />} />
            </Routes>
          </BrowserRouter>
        </TooltipProvider>
      </QueryClientProvider>
    </IdentityGate>
  </IdentityProvider>
);

export default App;

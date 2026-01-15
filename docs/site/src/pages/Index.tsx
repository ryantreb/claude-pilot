import NavBar from "@/components/NavBar";
import HeroSection from "@/components/HeroSection";
import ComparisonSection from "@/components/ComparisonSection";
import WorkflowSteps from "@/components/WorkflowSteps";
import WhatsInside from "@/components/WhatsInside";
import InstallSection from "@/components/InstallSection";
import LicensingSection from "@/components/LicensingSection";
import Footer from "@/components/Footer";
import SEO from "@/components/SEO";

const Index = () => {
  const breadcrumbStructuredData = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://www.claude-code.pro"
      }
    ]
  };

  const softwareStructuredData = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Claude CodePro",
    "description": "Professional Development Environment for Claude Code - Automated Context Management, Spec-Driven Development, Skills, TDD, LSP, Semantic Search, Persistent Memory, Quality Hooks, and Modular Rules System.",
    "applicationCategory": "DeveloperApplication",
    "operatingSystem": "Linux, macOS, Windows (via Docker)",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    },
    "author": {
      "@type": "Person",
      "name": "Max Ritter",
      "url": "https://maxritter.net/"
    },
    "license": "https://www.gnu.org/licenses/agpl-3.0",
    "url": "https://github.com/maxritter/claude-codepro",
    "downloadUrl": "https://github.com/maxritter/claude-codepro"
  };

  return (
    <>
      <SEO
        title="Claude CodePro - Professional Development Environment for Claude Code"
        description="Start shipping systematically with Automated Context Management, Spec-Driven Development, Skills, TDD, LSP, Semantic Search, Persistent Memory, Quality Hooks, and more. Free for individuals, commercial license for companies."
        structuredData={[breadcrumbStructuredData, softwareStructuredData]}
      />
      <NavBar />
      <main className="min-h-screen bg-background">
        <HeroSection />
        <InstallSection />
        <WhatsInside />
        <ComparisonSection />
        <WorkflowSteps />
        <LicensingSection />
        <Footer />
      </main>
    </>
  );
};

export default Index;

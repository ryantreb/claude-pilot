import * as React from "react";

import { cn } from "@/lib/utils";

const Input = React.forwardRef<HTMLInputElement, React.ComponentProps<"input">>(
  ({ className, type, ...props }, ref) => {
    return (
      <input
        type={type}
        className={cn(
          "flex h-10 w-full rounded-[10px] border border-border bg-background px-3 py-2 text-base ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm [box-shadow:inset_0px_2px_4px_0px_rgba(0,_0,_0,_0.3),_0px_1px_2px_0px_rgba(255,_255,_255,_0.05)] hover:[box-shadow:inset_0px_2px_4px_0px_rgba(0,_0,_0,_0.4),_0px_1px_2px_0px_rgba(255,_255,_255,_0.08)] focus-visible:[box-shadow:inset_0px_2px_4px_0px_rgba(0,_0,_0,_0.3),_0px_0px_0px_2px_hsl(209_72%_63%_/_30%)] transition-all duration-200",
          className
        )}
        ref={ref}
        {...props}
      />
    );
  }
);
Input.displayName = "Input";

export { Input };

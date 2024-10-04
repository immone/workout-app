"use client";
import { zodResolver } from "@hookform/resolvers/zod";
import { format } from "date-fns";
import { CalendarIcon } from "lucide-react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import * as React from "react";

import { cn } from "@/lib/utils";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
} from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";

const FormSchema = z.object({
  selectedDates: z.array(z.date()).nonempty({
    message: "Please select at least one date.",
  }),
});

const SimpleCalendarForm: React.FC<{
  onDateSelection: (dates: Date[]) => void;
  onToastMessage: (message: string) => void;
}> = ({ onDateSelection, onToastMessage }) => {
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      selectedDates: [],
    },
  });

  const onSubmit = (data: z.infer<typeof FormSchema>) => {
    const validDates = data.selectedDates.filter(date => date instanceof Date && !isNaN(date.getTime()));

    if (validDates.length === 0) {
      onToastMessage("Please select at least one valid date.");
      return;
    }

    const earliestDate = new Date(Math.min(...validDates.map(date => date.getTime())));
    
    let formattedDates: string;
    if (validDates.length === 1) {
      formattedDates = format(validDates[0], "PPP");
    } else if (validDates.length === 2) {
      formattedDates = `${format(validDates[0], "PPP")} and ${format(validDates[1], "PPP")}`;
    } else {
      formattedDates = `${format(earliestDate, "PPP")} + ${validDates.length - 1} more`;
    }
    
    onToastMessage(`You selected the following dates: ${formattedDates}`);
    onDateSelection(validDates);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
        <FormField
          control={form.control}
          name="selectedDates"
          render={({ field }) => (
            <FormItem className="flex flex-col">
              <FormLabel className="text-white">Select dates</FormLabel>
              <Popover>
                <PopoverTrigger asChild>
                  <FormControl>
                    <Button
                      variant={"outline"}
                      className={cn(
                        "w-[240px] pl-3 text-left font-normal text-white border border-white bg-transparent hover:bg-white hover:bg-opacity-10",
                        field.value.length === 0 && "text-muted-foreground"
                      )}
                    >
                      {field.value.length > 0 ? (
                        format(field.value[0], "PPP") + 
                        (field.value.length > 1 ? ` + ${field.value.length - 1} more` : "")
                      ) : (
                        <span className="text-gray-400">Pick dates</span>
                      )}
                      <CalendarIcon className="ml-auto h-4 w-4 text-white opacity-50" />
                    </Button>
                  </FormControl>
                </PopoverTrigger>
                <PopoverContent className="w-auto p-0" align="start" side="bottom">
                  <Calendar
                    mode="multiple"
                    selected={field.value}
                    onSelect={(date) => {
                      if (!date) return;
                      if (Array.isArray(date)) {
                        field.onChange(date);
                      } else {
                        const newDates = field.value.includes(date)
                          ? field.value.filter(d => d !== date)
                          : [...field.value, date];
                        field.onChange(newDates);
                      }
                    }}
                    className="custom-calendar rounded-md"
                  />
                </PopoverContent>
              </Popover>
              <FormDescription className="text-gray-300">
                Your selected dates will be recorded.
              </FormDescription>
            </FormItem>
          )}
        />
        <Button 
          type="submit" 
          className="bg-green-500 text-white rounded-corners w-full transition duration-200 hover:bg-blue-600 mb-4">
          Submit
        </Button>
      </form>
    </Form>
  );
};

export default SimpleCalendarForm;

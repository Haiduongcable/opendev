import { useEffect, useRef, useState, useCallback, useMemo } from 'react';
import { useChatStore } from '../../stores/chat';
import { WelcomeScreen } from './WelcomeScreen';
import { ProgressIndicator } from './ProgressIndicator';
import { MessageItem } from './MessageItem';

// ⚡ Bolt Performance Optimization:
// Use a stable reference for empty fallback arrays to prevent Zustand selectors
// from returning a new array instance on every state change, which would trigger
// unnecessary deep re-renders of the MessageList component.
const EMPTY_ARRAY: any[] = [];

export function MessageList() {
  const messages = useChatStore(state => {
    const sid = state.currentSessionId;
    return sid ? state.sessionStates[sid]?.messages ?? EMPTY_ARRAY : EMPTY_ARRAY;
  });
  const isLoading = useChatStore(state => {
    const sid = state.currentSessionId;
    return sid ? state.sessionStates[sid]?.isLoading ?? false : false;
  });
  const progressMessage = useChatStore(state => {
    const sid = state.currentSessionId;
    return sid ? state.sessionStates[sid]?.progressMessage ?? null : null;
  });
  const thinkingLevel = useChatStore(state => state.thinkingLevel);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const scrollContainerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll state
  const [userHasScrolled, setUserHasScrolled] = useState(false);
  const isNearBottomRef = useRef(true);

  // Stagger animation: track previous message count
  const prevMessageCountRef = useRef(messages.length);

  // Smart auto-scroll: track user scroll position
  const scrollTicking = useRef(false);
  const handleScroll = useCallback(() => {
    if (!scrollTicking.current) {
      scrollTicking.current = true;
      requestAnimationFrame(() => {
        const container = scrollContainerRef.current;
        if (!container) {
          scrollTicking.current = false;
          return;
        }

        const distanceFromBottom = container.scrollHeight - container.scrollTop - container.clientHeight;
        const nearBottom = distanceFromBottom < 50;

        isNearBottomRef.current = nearBottom;

        if (nearBottom) {
          setUserHasScrolled(false);
        } else {
          setUserHasScrolled(true);
        }

        scrollTicking.current = false;
      });
    }
  }, []);

  useEffect(() => {
    if (!userHasScrolled) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, userHasScrolled, progressMessage]);

  // Update stagger ref after new messages settle
  useEffect(() => {
    const timer = setTimeout(() => {
      prevMessageCountRef.current = messages.length;
    }, 500);
    return () => clearTimeout(timer);
  }, [messages.length]);

  // Custom Page Up/Page Down handling with shorter scroll distance
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!scrollContainerRef.current) return;

      const scrollDistance = 300; // Shorter scroll distance (default is ~viewport height)

      if (e.key === 'PageUp') {
        e.preventDefault();
        scrollContainerRef.current.scrollBy({
          top: -scrollDistance,
          behavior: 'smooth'
        });
      } else if (e.key === 'PageDown') {
        e.preventDefault();
        scrollContainerRef.current.scrollBy({
          top: scrollDistance,
          behavior: 'smooth'
        });
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // ⚡ Bolt Performance Optimization:
  // Memoize the mapping of MessageItem components to prevent O(N) JSX recreation
  // during frequent scroll events or unrelated UI state changes (like progressMessage updates).
  const renderedMessages = useMemo(() => {
    return messages.map((message, index) => {
      const isLastMessage = index === messages.length - 1;
      return (
        <MessageItem
          key={index}
          message={message}
          index={index}
          isNewMessage={index >= prevMessageCountRef.current}
          prevMessageCount={prevMessageCountRef.current}
          thinkingLevel={thinkingLevel}
          // Only pass isLoading to the very last message to prevent re-rendering all messages when loading toggles
          isLoading={isLastMessage ? isLoading : false}
          isLastMessage={isLastMessage}
        />
      );
    });
  }, [messages, thinkingLevel, isLoading]);

  if (messages.length === 0) {
    return <WelcomeScreen />;
  }

  return (
    <div ref={scrollContainerRef} className="flex-1 overflow-y-auto bg-bg-100" onScroll={handleScroll}>
      <div className="max-w-5xl mx-auto py-6 px-4 md:px-8 space-y-4">
        {renderedMessages}

        {/* Progress indicator */}
        {(progressMessage || isLoading) && (
          <ProgressIndicator progressMessage={progressMessage} />
        )}

        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
